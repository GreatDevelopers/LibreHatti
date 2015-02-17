from django.contrib import admin
from django.contrib.auth.admin import *
from librehatti.Test_Reports.forms import *

from django.http import HttpResponseRedirect

from librehatti.Test_Reports.models import *
from django.core.urlresolvers import reverse
    
admin.autodiscover()

class Test_Reports_inline(admin.StackedInline):
    model = Test_Report_Descriptions
    form = Test_Reports_Des
    fields = ['Description', 'Start_Date', 'Strength','mix']
    extra = 30

class Test_Reports_Admin(admin.ModelAdmin):
    inlines = [Test_Reports_inline]
    model = Test_Reports
    def response_add(self, request, obj, post_url_continue=None):
        request.session['data'] = request.POST
        return HttpResponseRedirect(reverse('librehatti.Test_Reports.views.Reports'))
 
admin.site.register(Test_Reports,Test_Reports_Admin)
    
