from django.forms import ModelForm
from models import TaDa

class TaDaForm(ModelForm):
	class Meta:
		model = TaDa
		#widgets = {
		#'departure_time_from_tcc': modelforms.TextInput('attrs'= { 'name' : 'list'})
		#'arrival_time_at_site': modelforms.TextInput('attrs'= { 'name' : 'list'})
		# }
		#name = {
        #    'departure_time_from_tcc': ('list'),
       # }
       # widgets = {
        #'departure_time_from_tcc': forms.TimeInput(format='%H:%M')
        #}
