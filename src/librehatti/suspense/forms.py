from django.forms import ModelForm
from models import TaDa
from django import forms

class TaDaSearch(forms.Form):
		ref_no = forms.IntegerField()

class TaDaForm(ModelForm):
	class Meta:
		model = TaDa

