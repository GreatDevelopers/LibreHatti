from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse

from librehatti.catalog.request_change import request_notify

from django.contrib.auth.decorators import login_required
from librehatti.suspense.models import *
from useraccounts.models import *
from librehatti.catalog.models import *

from librehatti.suspense.models import Staff

from librehatti.programmeletter.models import LetterData
from librehatti.programmeletter.models import StaffInTeam
from django.contrib.auth.models import User
from librehatti.catalog.models import HeaderFooter
from django.utils.datastructures import MultiValueDictKeyError
import simplejson


@login_required
def programmeletter(request):
    old_post = request.session.get('old_post')
    buyer_name = User.objects.values( \
    'first_name','last_name','id').get(id=old_post['buyer'])
    street_address = Address.objects.values( \
    'street_address','city','pin','province').get(id=buyer_name['id'])
    old_post = request.session.get('old_post')
    letterdata_id = request.session.get('letterdata_id')
    letterdata = LetterData.objects.values('team_name', \
        'team_name__team_name','vehicle__vehicle_no',  \
        'vehicle__vehicle_name', 'letter_date')
    get(id=letterdata_id)
    staffinteam = StaffInTeam.objects.values('team_name__team_name',
        'staff__name').filter(team_name=letterdata['team_name'])
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'programmeletter/programmeletter.html',
        {'header':header, 'data':old_post, 'vehicle':letterdata,
        'staffinteam':staffinteam, 'buyer':buyer_name,\
        'address':street_address})

def programmerletter_details(request):  
    buyer_name = User.objects.values( \
    'first_name','last_name','id').get(id =request.GET.get("item_id"))
    buyer_full_name = buyer_name['first_name']+" "+\
    buyer_name['last_name']
    buyer_phone = Customer.objects.values( \
    'telephone').get(id =request.GET.get("item_id"))
    buyer_full_telephone = buyer_phone['telephone']
    buyer_full_name += "&"+buyer_full_telephone
    return HttpResponse(buyer_full_name)
