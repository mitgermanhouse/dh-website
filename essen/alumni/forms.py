from django import forms

class AddAlumniForm(forms.Form):
    xlsx_file = forms.FileField(label='Select XLSX File')
