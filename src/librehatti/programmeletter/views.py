from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from librehatti.catalog.request_change import request_notify

from django.contrib.auth.decorators import login_required

from librehatti.suspense.models import Staff

from librehatti.programmeletter.models import LetterData
from librehatti.programmeletter.models import StaffInTeam

from librehatti.catalog.models import HeaderFooter

import simplejson


@login_required
def programmeletter(request):
    """
    This view generates the programme letter after filling the required data
    for letter.
    Argument:Http Request
    Return:Render Letter
    """
    old_post = request.session.get('old_post')
    letterdata_id = request.session.get('letterdata_id')
    letterdata = LetterData.objects.values('team_name', 'team_name__team_name',
        'vehicle__vehicle_no', 'vehicle__vehicle_name', 'letter_date').\
    get(id=letterdata_id)
    staffinteam = StaffInTeam.objects.values('team_name__team_name',
        'staff__name').filter(team_name=letterdata['team_name'])
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'programmeletter/programmeletter.html',
        {'header':header, 'data':old_post, 'vehicle':letterdata,
        'staffinteam':staffinteam})
