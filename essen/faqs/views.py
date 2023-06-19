from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from faqs.forms import FaqForm
from faqs.models import Faq


class FaqsListView(ListView):
    template_name = "faqs/index.html"
    queryset = (
        Faq.objects.all()
        .select_related("category")
        .only("question", "id", "category__name", "category__color")
        .order_by(Lower("category__name"), Lower("question"))
    )
    context_object_name = "faq_list"


class FaqDetailView(DetailView):
    template_name = "faqs/detail.html"
    model = Faq
    context_object_name = "faq"


class FaqEditView(PermissionRequiredMixin, DetailView):
    template_name = "faqs/edit_faq.html"
    model = Faq
    context_object_name = "faq"

    permission_required = "faqs.change_faq"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faq = self.object  # Can be None

        # Modify context
        context["faq_form"] = FaqForm(instance=faq, label_suffix="")

        if faq is not None:
            context["faq"] = faq

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        faq = self.get_object()

        # Save Faq
        faq_form = FaqForm(instance=faq, data=request.POST)
        faq = faq_form.save()

        return HttpResponseRedirect(reverse("faqs:detail", args=[faq.pk]))


class FaqAddView(FaqEditView):
    permission_required = "faqs.add_faq"

    def get_object(self):
        return None


class FaqDeleteView(PermissionRequiredMixin, DetailView):
    permission_required = "faqs.delete_faq"
    model = Faq
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return HttpResponseRedirect(reverse("faqs:index"))
