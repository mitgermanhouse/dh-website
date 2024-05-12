from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Hidden, Layout, Row, Submit
from django import forms
from menu.models import MealDayTime

from essen.helper import compress_image_upload
from home.models import Member, Plushie


class NonClearableImageField(forms.fields.ImageField):
    widget = forms.widgets.FileInput


class MemberDataForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("class_year", "major", "bio")

        labels = {"class_year": "Class Year", "major": "Major", "bio": "About Yourself"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row("class_year", "major", css_class="row-cols-1 row-cols-lg-2"),
            Field("bio", rows="4"),
            Div(
                Submit("data_form", "Save"),
                css_class="d-grid d-md-flex justify-content-md-end",
            ),
        )


class MemberImageForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("image",)

        field_classes = {"image": NonClearableImageField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "image_form"

    def clean_image(self):
        image = self.cleaned_data.get("image")
        return compress_image_upload(image)


class MemberDiningForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("auto_lateplates", "dietary_restrictions")

        labels = {
            "auto_lateplates": "Automatic Lateplates",
            "dietary_restrictions": "Dietary Restrictions",
        }

        widgets = {
            "auto_lateplates": forms.CheckboxSelectMultiple,
            "dietary_restrictions": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["auto_lateplates"].queryset = MealDayTime.objects.order_by(
            *MealDayTime.day_time_order
        )

        self.helper = FormHelper()
        self.helper.label_class = "h6"

        self.helper.layout = Layout(
            Row(
                Column("auto_lateplates", css_class="col-6"),
                Column("dietary_restrictions", css_class="col-6"),
            ),
            Div(
                Submit(None, "Update"),
                css_class="d-grid d-md-flex justify-content-md-end",
            ),
        )


class MemberCreateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("class_year", "major", "bio", "image")

        labels = {
            "class_year": "Class Year",
            "major": "Major",
            "bio": "About Yourself",
            "image": "Profile Picture",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row("class_year", "major", css_class="row-cols-1 row-cols-lg-2"),
            Field("bio", rows="4"),
            "image",
            Div(
                Submit(None, "Save"),
                css_class="d-grid d-md-flex justify-content-md-end",
            ),
        )


class PlushieForm(forms.ModelForm):
    class Meta:
        model = Plushie
        fields = ("name", "bio", "image")

        labels = {
            "name": "Name",
            "bio": "About",
            "image": "Picture",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Hidden("type", "plushie"),
            Row("name"),
            Field("bio", rows="4"),
            "image",
        )

        if instance := kwargs.get("instance"):
            self.helper.form_id = f"plushie_edit_{instance.id}"
        else:
            self.helper.form_id = "plushie_create"

    def clean_image(self):
        image = self.cleaned_data.get("image")
        return compress_image_upload(image)
