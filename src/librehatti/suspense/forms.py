from django.forms import ModelForm,TextInput
from models import TaDa
from django import forms
from django.utils.translation import ugettext_lazy as _


class TaDaSearch(forms.Form):
    ref_no = forms.IntegerField()

class TaDaForm(ModelForm):
	class Meta:
		model = TaDa
        #widgets = {
		#'suspense' : TextInput(attrs={'size':10}),
        # }
       
        
