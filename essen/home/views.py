from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from home.models import Member
from home.forms import MemberDataForm, MemberImageForm, MemberDiningForm, MemberCreateForm

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.exclude(user__groups__name__in=['alumni']).order_by('class_year', '-user')
        return context


class ProfileCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberCreateForm
    template_name = 'home/create_profile.html'
    success_url = reverse_lazy('home:home')

    def setup(self, request, *args, **kwargs):
        if hasattr(request.user, 'member'):
            messages.warning(request, '<b>WARNING:</b> You already have a profile.')
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, form):
        return f'Welcome {self.request.user.get_full_name()}! Your profile was created sucessfully.'


# REFERENCE: https://chriskief.com/2012/12/30/django-class-based-views-with-multiple-forms/
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'home/edit_profile.html'
    form_class = MemberDataForm
    image_form_class = MemberImageForm
    context_object_name = 'member'
    success_url = reverse_lazy('home:edit_profile')
    success_message = 'Your profile was updated sucessfully.'

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'member'):
            return user.member
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Modify context
        context['edit_access'] = check_if_profile_edit_access(self.request.user)

        if 'data_form' not in context:
            context['data_form'] = self.form_class(instance=self.object)
        if 'image_form' not in context:
            context['image_form'] = self.image_form_class(instance=self.object)

        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'data_form' in request.POST:
            form_class = self.form_class
            form_name = 'data_form'
        else:
            form_class = self.image_form_class
            form_name = 'image_form'

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})
    

class DiningUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'home/edit_dining.html'
    context_object_name = 'member'
    form_class = MemberDiningForm
    success_url = reverse_lazy('home:edit_dining')
    success_message = 'Your dining preferences were updated sucessfully.'

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'member'):
            return user.member
        else:
            raise Http404


def check_if_profile_edit_access(user):
    # users under profile ban will not be allowed to edit their profiles (for trolling prevention)
    return user.groups.filter(name='profile_ban').count() == 0
