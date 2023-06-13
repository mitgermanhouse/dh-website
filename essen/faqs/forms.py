from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from essen.widgets import Select2Widget
from faqs.models import Faq


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ("question", "answer", "category")

        labels = {
            "question": "Question",
            "answer": "Answer",
            "category": "Category",
        }

        widgets = {"category": Select2Widget(data_values=["color", "color_is_light"])}

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.fields["category"].empty_label = "- None -"

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-2"
        self.helper.field_class = "col-md-10"

        self.helper.layout = Layout(
            "question",
            "answer",
            Field("category", css_class="select2category"),
        )
