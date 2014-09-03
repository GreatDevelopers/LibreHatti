from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponse
from librehatti.voucher.models import *
from librehatti.catalog.models import PurchaseOrder

"""
This function calculates the session id and then initialise or increment 
voucher number according to the previous purchase order's session id
"""
def voucher_generate(request):
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    suffix = "/search_result/?search="
    prefix = "&Order=Order+Search"
    url = suffix + str(purchase_order_id) + prefix
    purchase_order = PurchaseOrder.objects.values('id','date_time').\
    get(id = purchase_order_id)
    purchase_order_id = purchase_order['id']
    purchase_order_date = purchase_order['date_time'].date()
    financialsession = FinancialSession.objects.\
    values('id','session_start_date','session_end_date')
    for value in financialsession:
        start_date = value['session_start_date']
        end_date = value['session_end_date']
        if start_date <= purchase_order_date <= end_date:
            session_id = value['id']
    pre_purchase_order_id = purchase_order_id - 1
    flag = 0
    while flag == 0:
        if pre_purchase_order_id == 0:
            session = FinancialSession.objects.get(id = session_id)
            poi = PurchaseOrder.objects.get(id = purchase_order_id)
            voucherid = VoucherId(purchase_order = poi, voucher_no = 1,\
            purchase_order_of_session = 1, purchased_item_of_session = 1,\
            session = session)
            voucherid.save()
            flag = 1
            return HttpResponseRedirect(url)
        else:
            try:
                voucherid = VoucherId.objects.values('voucher_no',\
                'purchase_order_of_session', 'purchased_item_of_session',\
                'session').get(purchase_order = pre_purchase_order_id)
                pre_purchase_order_session = voucherid['session']
                if session_id == pre_purchase_order_session:
                    voucher_no = voucherid['voucher_no'] + 1
                    purchase_order_of_session = voucherid[\
                    'purchase_order_of_session'] + 1
                    purchased_item_of_session = voucherid[\
                    'purchased_item_of_session'] + 1
                    session = FinancialSession.objects.get(id = session_id)
                    poi = PurchaseOrder.objects.get(id = purchase_order_id)
                    voucherid = VoucherId(purchase_order = poi,\
                    voucher_no = voucher_no,\
                    purchase_order_of_session = purchase_order_of_session,\
                    purchased_item_of_session = purchased_item_of_session,\
                    session = session)
                    voucherid.save()
                    flag = 1
                    return HttpResponseRedirect(url)
                else:
                    session = FinancialSession.objects.get(id = session_id)
                    poi = PurchaseOrder.objects.get(id = purchase_order_id)
                    voucherid = VoucherId(purchase_order = poi, voucher_no = 1,\
                    purchase_order_of_session = 1,\
                    purchased_item_of_session = 1, session = session)
                    voucherid.save()
                    flag = 1
                    return HttpResponseRedirect(url)
            except:
                pre_purchase_order_id = pre_purchase_order_id - 1
