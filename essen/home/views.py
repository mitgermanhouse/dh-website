from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

from home.forms import (
    MemberCreateForm,
    MemberDataForm,
    MemberDiningForm,
    MemberImageForm,
    PlushieForm,
)
from home.models import GalleryContent, Member, Plushie


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = (
            Member.objects.filter(user__is_active=True)
            .order_by("class_year", "-user")
            .select_related("user")
        )
        context["plushies"] = (
            Plushie.objects.filter(member__user__is_active=True)
            .order_by("member__class_year", "-member__user", "name")
            .all()
        )
        context["galleryContent"] = GalleryContent.objects.all()
        return context


class ProfileCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberCreateForm
    template_name = "home/create_profile.html"
    success_url = reverse_lazy("home:home")

    def setup(self, request, *args, **kwargs):
        if hasattr(request.user, "member"):
            messages.warning(request, "<b>WARNING:</b> You already have a profile.")
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, form):
        return (
            f"Welcome {self.request.user.get_full_name()}! Your profile was created"
            " sucessfully."
        )


# REFERENCE: https://chriskief.com/2012/12/30/django-class-based-views-with-multiple-forms/
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "home/edit_profile.html"
    form_class = MemberDataForm
    image_form_class = MemberImageForm
    plushie_form_class = PlushieForm
    context_object_name = "member"
    success_url = reverse_lazy("home:edit_profile")
    success_message = "Your profile was updated successfully."

    def get_object(self):
        user = self.request.user
        if hasattr(user, "member"):
            return user.member
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Modify context
        context["edit_access"] = check_if_profile_edit_access(self.request.user)

        if "data_form" not in context:
            context["data_form"] = self.form_class(instance=self.object)
        if "image_form" not in context:
            context["image_form"] = self.image_form_class(instance=self.object)
        if "plushie_edit_forms" not in context:
            plushie_edit_forms = []
            for plushie in self.object.plushie_set.order_by("name").all():
                plushie_edit_form = self.plushie_form_class(instance=plushie)
                plushie_edit_form.helper.form_action = reverse(
                    "home:edit_plushie", args=[plushie.pk]
                )
                plushie_edit_forms.append(plushie_edit_form)
            context["plushie_edit_forms"] = plushie_edit_forms
        if "plushie_create_form" not in context:
            plushie_create_form = self.plushie_form_class()
            plushie_create_form.helper.form_action = reverse("home:add_plushie")
            context["plushie_create_form"] = plushie_create_form

        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if "data_form" in request.POST:
            form_class = self.form_class
            form_name = "data_form"
        elif "image_form" in request.POST:
            form_class = self.image_form_class
            form_name = "image_form"
        else:
            raise ValueError("Invalid form type")

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, form.errors)
            return self.form_invalid(**{form_name: form})


class PlushieEditView(View, LoginRequiredMixin, SingleObjectMixin):
    model = Plushie
    success_message = "Plushie updated"
    redirect_url = reverse_lazy("home:edit_profile")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        plushie = self.get_object()
        member = request.user.member

        if plushie is not None and plushie.member.user != request.user:
            messages.error(
                request, "You are not allowed to edit someone else's plushie"
            )
            return HttpResponseRedirect(self.redirect_url)

        form = PlushieForm(instance=plushie, data=request.POST, files=request.FILES)

        if form.is_valid():
            if plushie is None:
                plushie = form.save(commit=False)
                plushie.member = member
                plushie.save()
            else:
                form.save()

            messages.success(request, self.success_message)
            return HttpResponseRedirect(self.redirect_url)
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(self.redirect_url)


class PlushieAddView(PlushieEditView):
    success_message = "Plushie added"

    def get_object(self, *args, **kwargs):
        return None


class PlushieDeleteView(PlushieEditView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        plushie = self.get_object()
        if plushie.member.user != request.user:
            messages.error(
                request, "You are not allowed to edit someone else's plushie"
            )
            return HttpResponseRedirect(self.redirect_url)
        plushie.delete()
        return HttpResponseRedirect(self.redirect_url)


class DiningUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "home/edit_dining.html"
    context_object_name = "member"
    form_class = MemberDiningForm
    success_url = reverse_lazy("home:edit_dining")
    success_message = "Your dining preferences were updated successfully."

    def get_object(self):
        user = self.request.user
        if hasattr(user, "member"):
            return user.member
        else:
            raise Http404


def check_if_profile_edit_access(user):
    # users under profile ban will not be allowed to edit their profiles
    # (for trolling prevention)
    return user.groups.filter(name="profile_ban").count() == 0
