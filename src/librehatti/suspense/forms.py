from django.forms import ModelForm,TextInput
from models import TaDa
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import SuspenseOrder


class TaDaSearch(forms.Form):
    ref_no = forms.ModelChoiceField(queryset= SuspenseOrder.objects.all())

class TaDaForm(ModelForm):
	class Meta:
		model = TaDa
        #widgets = {
		#'suspense' : TextInput(attrs={'size':10}),
        # }
       
        
