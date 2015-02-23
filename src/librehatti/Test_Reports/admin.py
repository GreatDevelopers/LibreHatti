from django.contrib import admin

from django.contrib.auth.admin import *

from librehatti.Test_Reports.forms import *

from django.http import HttpResponseRedirect

from librehatti.Test_Reports.models import *

from django.core.urlresolvers import reverse
    
admin.autodiscover()


class Test_Reports_Inline(admin.StackedInline):
    model = Test_Report_Descriptions
    form = Test_Reports_Des
    fields = ['Description', 'Start_Date', 'Strength','mix']
    extra = 30

class Soil_building_Inline(admin.StackedInline):
    model = Soil_building_des
    form = Soil_building_Des
    fields = ['Dt','Ob_Pr','Corr_F','Ob_N_V','Corr_N_V']
    extra = 30
    

class Test_Reports_Admin(admin.ModelAdmin):
    inlines = [Test_Reports_Inline]
    model = Test_Reports


    def response_add(self, request, obj, post_url_continue=None):
        request.session['data'] = request.POST
        return HttpResponseRedirect(reverse('librehatti.Test_Reports.views.Reports'))

class Soil_building_Admin(admin.ModelAdmin):
    inlines = [Soil_building_Inline]
    model = Soil_building

    def response_add(self, request, obj, post_url_continue=None):
        request.session['data'] = request.POST
        return HttpResponseRedirect(reverse('librehatti.Test_Reports.views.Soil_building'))


admin.site.register(Test_Reports,Test_Reports_Admin)
admin.site.register(Soil_building,Soil_building_Admin)
