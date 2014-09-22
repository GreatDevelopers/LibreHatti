from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponse
from librehatti.voucher.models import *
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Bill
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.models import TaxesApplied
from useraccounts.models import Address
from django.db.models import Max, Sum
from librehatti.prints.helper import num2eng
from librehatti.suspense.models import SuspenseOrder, Staff
from django.core.urlresolvers import reverse

"""
This function calculates the session id and then initialise or increment 
voucher number according to the previous purchase order's session id
"""
def voucher_generate(request):
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    
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
    purchased_item = PurchasedItem.objects.values_list('item__category',\
    flat=True).filter(purchase_order = purchase_order_id).\
    order_by('item__category')
    purchased_item_id = PurchasedItem.objects.values_list('id',\
    flat=True).filter(purchase_order = purchase_order_id).\
    order_by('item__category')
    voucherno = 0
    purchaseditemofsession = 0
    item = 0
    session = FinancialSession.objects.get(id = session_id)
    poi = PurchaseOrder.objects.get(id = purchase_order_id)
    max_id = VoucherId.objects.all().aggregate(Max('id'))
    if max_id['id__max'] == None:
        voucherno = 1
        purchaseditemofsession = 1
        for value in purchased_item:
            distribution_type = CategoryDistributionType.objects.\
            values('distribution').get(category = purchased_item[item])
            distribution = Distribution.objects.\
            values('id','ratio','college_income','admin_charges').\
            get(id = distribution_type['distribution'])
            distribution_id = Distribution.objects.\
            get(id = distribution_type['distribution'])
            voucherid = VoucherId(purchase_order = poi,\
            purchased_item = PurchasedItem.objects.get(pk = purchased_item_id[item]),\
            voucher_no = voucherno,purchase_order_of_session = 1,\
            purchased_item_of_session = purchaseditemofsession,\
            session = session, distribution = distribution_id,\
            ratio = distribution['ratio'],\
            college_income = distribution['college_income'], \
            admin_charges = distribution['admin_charges'])
            voucherid.save()
            try:
                purchaseditem = purchased_item[item+1]
                if purchased_item[item] == purchased_item[item+1]:
                    purchaseditemofsession = purchaseditemofsession + 1
                    item = item + 1
                else:
                    voucherno = voucherno + 1
                    purchaseditemofsession = purchaseditemofsession + 1
                    item = item + 1
            except:
                continue
    else:
        voucherid = VoucherId.objects.values('voucher_no',\
        'purchase_order_of_session', 'purchased_item_of_session',\
        'session').get(id = max_id['id__max'])
        pre_purchase_order_session = voucherid['session']
        voucher_no = voucherid['voucher_no']
        purchase_order_of_session = voucherid[\
        'purchase_order_of_session'] + 1
        purchased_item_of_session = voucherid[\
        'purchased_item_of_session']
        if session_id == pre_purchase_order_session:
            voucherno = voucher_no + 1
            purchaseditemofsession = purchased_item_of_session + 1
            for value in purchased_item:
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item[item])
                distribution = Distribution.objects.\
                values('id','ratio','college_income','admin_charges').\
                get(id = distribution_type['distribution'])
                distribution_id = Distribution.objects.\
                get(id = distribution_type['distribution'])
                voucherid = VoucherId(purchase_order = poi,\
                purchased_item = PurchasedItem.objects.get(pk = purchased_item_id[item]),\
                voucher_no = voucherno,\
                purchase_order_of_session = purchase_order_of_session,\
                purchased_item_of_session = purchaseditemofsession,\
                session = session, distribution = distribution_id,\
                ratio = distribution['ratio'],\
                college_income = distribution['college_income'],\
                admin_charges = distribution['admin_charges'])
                voucherid.save()
                try:
                    purchaseditem = purchased_item[item+1]
                    if purchased_item[item] == purchased_item[item+1]:
                        purchaseditemofsession = purchaseditemofsession + 1
                        item = item + 1
                    else:
                        voucherno = voucherno + 1
                        purchaseditemofsession = purchaseditemofsession + 1
                        item = item + 1
                except:
                    continue
        else:
            voucherno = 1
            purchaseditemofsession = 1
            for value in purchased_item:
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item[item])
                distribution = Distribution.objects.\
                values('id','ratio','college_income','admin_charges').\
                get(id = distribution_type['distribution'])
                distribution_id = Distribution.objects.\
                get(id = distribution_type['distribution'])
                voucherid = VoucherId(purchase_order = poi,\
                purchased_item = PurchasedItem.objects.get(pk = purchased_item_id[item]),\
                voucher_no = voucherno,\
                purchase_order_of_session = purchase_order_of_session,\
                purchased_item_of_session = purchaseditemofsession,\
                session = session, distribution = distribution_id,\
                ratio = distribution['ratio'],\
                college_income = distribution['college_income'],\
                admin_charges = distribution['admin_charges'])
                voucherid.save()
                try:
                    p = purchased_item[item+1]
                    if purchased_item[item] == purchased_item[item+1]:
                        purchaseditemofsession = purchaseditemofsession + 1
                        item = item + 1
                    else:
                        voucherno = voucherno + 1
                        purchaseditemofsession = purchaseditemofsession + 1
                        item = item + 1
                except:
                    continue
    voucher_obj = VoucherId.objects.values_list('id', flat=True).\
    filter(purchase_order = purchase_order_id).order_by('id')
    voucher_obj1 = VoucherId.objects.values_list('purchased_item', flat=True).\
    filter(purchase_order = purchase_order_id).order_by('id')
    voucher_obj2 = VoucherId.objects.values_list('voucher_no', flat=True).\
    filter(purchase_order = purchase_order_id).order_by('id')
    i = 0
    price = 0
    flag = 0
    for value in voucher_obj:
        purchased_item_obj = PurchasedItem.objects.\
        values('price','item__category').get(purchase_order = purchase_order_id,\
        id = voucher_obj1[i])
        try:
            voucher_number = voucher_obj[i+1]
            if voucher_obj2[i] == voucher_obj2[i+1]:
                price_item = purchased_item_obj['price']
                price = price + price_item
                i = i + 1
                flag = 0
            else:
                price_item = purchased_item_obj['price']
                price = price + price_item
                voucher_number = voucher_obj2[i]
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = (price * distribution_obj['college_income'])/100
                cost_admin_charges = (price * distribution_obj['admin_charges'])/100
                remain_cost = price - (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = (remain_cost * int(split[0]))/100
                cost_development_fund = (remain_cost * int(split[1]))/100
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number, \
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund,\
                total = price, session = session)
                calculate_distribution.save()
                price = 0
                flag = 1
                i = i + 1
        except:
            if flag == 0:
                price_item = purchased_item_obj['price']
                price = price + price_item
                voucher_number = voucher_obj2[i]
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = (price * distribution_obj['college_income'])/100
                cost_admin_charges = (price * distribution_obj['admin_charges'])/100
                remain_cost = price - (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = (remain_cost * int(split[0]))/100
                cost_development_fund = (remain_cost * int(split[1]))/100
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number,\
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund, total = price,\
                session = session)
                calculate_distribution.save()
            else:
                price = 0
                price_item = purchased_item_obj['price']
                price = price + price_item
                voucher_number = voucher_obj2[i]
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = (price * distribution_obj['college_income'])/100
                cost_admin_charges = (price * distribution_obj['admin_charges'])/100
                remain_cost = price - (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = (remain_cost * int(split[0]))/100
                cost_development_fund = (remain_cost * int(split[1]))/100
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number,\
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund, total = price,\
                session = session)
                calculate_distribution.save()
    request.session['old_post'] = old_post
    request.session['purchase_order_id'] = purchase_order_id
    return HttpResponseRedirect(reverse("librehatti.suspense.views.add_distance"))


def voucher_show(request):
    id = request.GET['order_id']
    purchase_order = PurchaseOrder.objects.get(id = id)
    voucher_no_list = []
    voucher_obj_distinct = []
    voucherid = VoucherId.objects.values('purchase_order','purchased_item', 'voucher_no', 'session').\
    filter(purchase_order = purchase_order)
    for value in voucherid:
        if value['voucher_no'] not in voucher_no_list:
            voucher_no_list.append(value['voucher_no'])
            voucher_obj_distinct.append(value)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'voucher/voucher_show.html', {'voucherid' : voucher_obj_distinct, 'header':header})


def voucher_print(request):
    number = request.GET['voucher_no']
    session = request.GET['session']
    purchase_order_id = request.GET['purchase_order']
    flag = 0
    voucherid = VoucherId.objects.values('voucher_no').filter(purchase_order = purchase_order_id)
    for value in voucherid:
        try:
            suspense_order = SuspenseOrder.objects.get(voucher = value['voucher_no'], purchase_order = purchase_order_id)
            flag = 1
        except:
            continue
    calculatedistribution = CalculateDistribution.objects.\
    values('college_income_calculated', 'admin_charges_calculated',\
    'consultancy_asset', 'development_fund', 'total').\
    get(voucher_no = number, session = session)
    total_in_words = num2eng(calculatedistribution['total'])
    voucherid = VoucherId.objects.values('purchase_order', 'ratio',\
    'college_income', 'admin_charges', 'distribution__name',\
    'purchased_item__item__category__name',\
    'purchased_item__item__category__parent__parent').\
    filter(voucher_no = number, session = session)
    for value in voucherid:
        purchase_order = value['purchase_order']
        distribution = value['distribution__name']
        ratio = value['ratio']
        college_income = value['college_income']
        admin_charges = value['admin_charges']
        category_name = value['purchased_item__item__category__name']
        lab_id = value['purchased_item__item__category__parent__parent']
    emp = Staff.objects.values('name','position').filter(lab=lab_id)
    purchase_order_obj = PurchaseOrder.objects.\
    values('date_time','buyer__first_name','buyer__last_name',\
    'delivery_address','tds').get(id = purchase_order)
    date = purchase_order_obj['date_time'].date()
    delivery_address = Address.objects.values('street_address','city','pin',\
    'province').get(id = purchase_order_obj['delivery_address'])
    bill = Bill.objects.values('delivery_charges','total_cost','grand_total','amount_received').get(purchase_order = purchase_order_id)
    amount_received_inwords = num2eng(bill['amount_received'])
    taxes_applied = TaxesApplied.objects.values('surcharge__tax_name','surcharge__value','tax').filter(purchase_order = purchase_order_id)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    if flag == 0:
        
        return render(request, 'voucher/voucher_report.html', {\
            'calculate_distribution' : calculatedistribution,\
            'admin_charges': admin_charges, 'college_income': college_income, \
            'ratio':ratio,'d_name': distribution, 'purchase_order': purchase_order,\
            'voucher':number, 'date': date,'address': delivery_address,\
            'buyer': purchase_order_obj, 'categoryname': category_name,\
            'total_in_words': total_in_words, 'employee' : emp, 'header': header})
        voucherid_obj = VoucherId.objects.values
    else:
        return render(request, 'voucher/voucher_report_suspence.html',{
            'address':delivery_address, 'cost':bill, 'inwords':amount_received_inwords,\
            'date':date, 'suspense_voucher':number, 'job':purchase_order_id,\
            'tds':purchase_order_obj, 'tax':taxes_applied, 'header': header})