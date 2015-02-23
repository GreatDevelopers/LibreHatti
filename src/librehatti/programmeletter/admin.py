from django.contrib import admin

from librehatti.programmeletter.models import TeamName
from librehatti.programmeletter.models import StaffInTeam
from librehatti.programmeletter.models import LetterData

from librehatti.programmeletter.forms import *

from ajax_select.admin import AjaxSelectAdmin

from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse


class StaffInline(admin.StackedInline):
    form = StaffInTeamForm
    model = StaffInTeam
    fields = ['staff', ]
    extra = 3


class TeamNameAdmin(AjaxSelectAdmin):
    form = TeamNameForm
    inlines = [StaffInline]
    model = TeamName


class LetterDataAdmin(AjaxSelectAdmin):
    form = LetterDataForm
    def response_add(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['letterdata_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("librehatti.programmeletter.views.programmeletter"))

    def response_change(self, request, obj, post_url_continue=None):
        request.session['old_post'] = request.POST
        request.session['letterdata_id'] = obj.id
        return HttpResponseRedirect(reverse\
            ("librehatti.programmeletter.views.programmeletter"))

admin.site.register(TeamName, TeamNameAdmin)
admin.site.register(LetterData, LetterDataAdmin)
