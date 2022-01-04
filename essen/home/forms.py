from django import forms
from django.contrib.auth.models import User
from home.models import Member


class NonClearableImageField(forms.fields.ImageField):
    widget = forms.widgets.FileInput

class MemberDataForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('class_year', 'major', 'bio')

        labels = {
            'class_year': 'Class Year',
            'major': 'Major',
            'bio': 'About Yourself'
        }

class MemberImageForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('image', )

        field_classes = {
            'image': NonClearableImageField
        }