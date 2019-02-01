from django.shortcuts import render

from django.http import  HttpResponseRedirect, HttpResponse

from librehatti.voucher.models import *

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Bill
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.models import TaxesApplied
from librehatti.catalog.models import SpecialCategories

from useraccounts.models import Address, Customer

from django.db.models import Max, Sum

from librehatti.prints.helper import num2eng

from librehatti.suspense.models import SuspenseOrder, Staff

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from librehatti.catalog.request_change import request_notify


@login_required
def voucher_generate(request):
    """
    This function calculates the session id and then initialise or increment
    voucher number according to the previous purchase order's session id
    Argument:Http Request
    Return:Response Redirect to add distance function
    """
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    generate_voucher = 1
    first_item = PurchasedItem.objects.values('item__category__id').\
    filter(purchase_order=purchase_order_id)[0]
    category_check = SpecialCategories.objects.filter(category=
        first_item['item__category__id'])
    if category_check:
        specialcategories = SpecialCategories.objects.values('voucher').\
        filter(category=first_item['item__category__id'])[0]
        if specialcategories['voucher'] == False:
            generate_voucher = 0
    purchase_order = PurchaseOrder.objects.values('id','date_time').\
    get(id = purchase_order_id)
    purchase_order_id = purchase_order['id']
    purchase_order_date = purchase_order['date_time']
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
        is_special_var = 0
        purchaseditemofsession = 1
        for value in purchased_item:
            if generate_voucher == 0:
                voucherno = 0
                is_special_var = 1
            distribution_type = CategoryDistributionType.objects.\
            values('distribution').get(category = purchased_item[item])
            distribution = Distribution.objects.\
            values('id','ratio','college_income','admin_charges').\
            get(id = distribution_type['distribution'])
            distribution_id = Distribution.objects.\
            get(id = distribution_type['distribution'])
            voucherid = VoucherId(purchase_order = poi,\
            purchased_item = PurchasedItem.objects.get\
            (pk = purchased_item_id[item]),voucher_no = voucherno,\
            purchase_order_of_session = 1,\
            purchased_item_of_session = purchaseditemofsession,\
            session = session, distribution = distribution_id,\
            ratio = distribution['ratio'],\
            college_income = distribution['college_income'], \
            admin_charges = distribution['admin_charges'],
            is_special=is_special_var)
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
        if voucherid['voucher_no'] == 0:
            temp_obj = VoucherId.objects.values('id').filter(is_special=0,
                session=session)
            if temp_obj:
                for temp_val in temp_obj:
                    maxid = temp_val['id']
                voucherid_temp = VoucherId.objects.values('voucher_no').\
                get(id=maxid)
                voucherid['voucher_no'] = voucherid_temp['voucher_no']
            else:
                voucherid['voucher_no'] = 0
        pre_purchase_order_session = voucherid['session']
        voucher_no = voucherid['voucher_no']
        purchase_order_of_session = voucherid[\
        'purchase_order_of_session'] + 1
        purchased_item_of_session = voucherid[\
        'purchased_item_of_session']
        if session_id == pre_purchase_order_session:
            voucherno = voucher_no + 1
            is_special_var = 0
            purchaseditemofsession = purchased_item_of_session + 1
            for value in purchased_item:
                if generate_voucher == 0:
                    voucherno = 0
                    is_special_var = 1
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item[item])
                distribution = Distribution.objects.\
                values('id','ratio','college_income','admin_charges').\
                get(id = distribution_type['distribution'])
                distribution_id = Distribution.objects.\
                get(id = distribution_type['distribution'])
                voucherid = VoucherId(purchase_order = poi,\
                purchased_item = PurchasedItem.objects.get\
                (pk = purchased_item_id[item]),\
                voucher_no = voucherno,\
                purchase_order_of_session = purchase_order_of_session,\
                purchased_item_of_session = purchaseditemofsession,\
                session = session, distribution = distribution_id,\
                ratio = distribution['ratio'],\
                college_income = distribution['college_income'],\
                admin_charges = distribution['admin_charges'],
                is_special=is_special_var)
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
            is_special_var = 0
            purchaseditemofsession = 1
            purchase_order_of_session = 1
            for value in purchased_item:
                if generate_voucher == 0:
                    voucherno = 0
                    is_special_var = 1
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').get(category = purchased_item[item])
                distribution = Distribution.objects.\
                values('id','ratio','college_income','admin_charges').\
                get(id = distribution_type['distribution'])
                distribution_id = Distribution.objects.\
                get(id = distribution_type['distribution'])
                voucherid = VoucherId(purchase_order = poi,\
                purchased_item = PurchasedItem.objects.get\
                (pk = purchased_item_id[item]),voucher_no = voucherno,\
                purchase_order_of_session = purchase_order_of_session,\
                purchased_item_of_session = purchaseditemofsession,\
                session = session, distribution = distribution_id,\
                ratio = distribution['ratio'],\
                college_income = distribution['college_income'],\
                admin_charges = distribution['admin_charges'],
                is_special=is_special_var)
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
        if generate_voucher == 0:
            break
        purchased_item_obj = PurchasedItem.objects.\
        values('price','item__category').\
        get(purchase_order = purchase_order_id,id = voucher_obj1[i])
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
                values('distribution').get\
                (category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = \
                round((price * distribution_obj['college_income'])/100)
                cost_admin_charges = \
                round((price * distribution_obj['admin_charges'])/100)
                remain_cost = price - \
                (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = round((remain_cost * int(split[0]))/100)
                cost_development_fund = round((remain_cost * int(split[1]))/100)
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number, \
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund,\
                total = price, session = session)
                calculate_distribution.save()
                voucher_total = VoucherTotal(voucher_no=voucher_number,\
                    session=session, total=price)
                voucher_total.save()
                price = 0
                flag = 1
                i = i + 1
        except:
            if flag == 0:
                price_item = purchased_item_obj['price']
                price = price + price_item
                voucher_number = voucher_obj2[i]
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').\
                get(category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = \
                round((price * distribution_obj['college_income'])/100)
                cost_admin_charges = \
                round((price * distribution_obj['admin_charges'])/100)
                remain_cost = \
                price - (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = round((remain_cost * int(split[0]))/100)
                cost_development_fund = round((remain_cost * int(split[1]))/100)
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number,\
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund, total = price,\
                session = session)
                calculate_distribution.save()
                voucher_total = VoucherTotal(voucher_no=voucher_number,\
                    session=session, total=price)
                voucher_total.save()
            else:
                price = 0
                price_item = purchased_item_obj['price']
                price = price + price_item
                voucher_number = voucher_obj2[i]
                distribution_type = CategoryDistributionType.objects.\
                values('distribution').\
                get(category = purchased_item_obj['item__category'])
                distribution_obj = Distribution.objects.\
                values('ratio', 'college_income', 'admin_charges').\
                get(id = distribution_type['distribution'])
                cost_college_income = \
                round((price * distribution_obj['college_income'])/100)
                cost_admin_charges = \
                round((price * distribution_obj['admin_charges'])/100)
                remain_cost = \
                price - (cost_college_income + cost_admin_charges)
                split = distribution_obj['ratio'].split(':')
                cost_consultancy_asset = round((remain_cost * int(split[0]))/100)
                cost_development_fund = round((remain_cost * int(split[1]))/100)
                calculate_distribution = CalculateDistribution(\
                voucher_no = voucher_number,\
                college_income_calculated = cost_college_income,\
                admin_charges_calculated = cost_admin_charges,\
                consultancy_asset = cost_consultancy_asset,\
                development_fund = cost_development_fund, total = price,\
                session = session)
                calculate_distribution.save()
                voucher_total = VoucherTotal(voucher_no=voucher_number,\
                    session=session, total=price)
                voucher_total.save()
    request.session['old_post'] = old_post
    request.session['purchase_order_id'] = purchase_order_id
    return HttpResponseRedirect(\
        reverse("suspense:add_distance"))


@login_required
def voucher_show(request):
    """
    This function shows the number of vouchers generated for a particular 
    order
    Argument:Http Request
    Return:Render Voucher Show
    """
    id = request.GET['order_id']
    purchase_order = PurchaseOrder.objects.get(id=id)
    voucher_no_list = []
    voucher_obj_distinct = []
    temp_voucherid = VoucherId.objects.values('voucher_no').\
    filter(purchase_order=purchase_order)[0]
    message = 'Voucher'
    if temp_voucherid['voucher_no'] == 0:
        message = "No voucher to display"
    voucherid = VoucherId.objects.values('purchase_order','purchased_item',\
        'voucher_no', 'session','purchase_order_of_session').\
    filter(purchase_order = purchase_order)
    for value in voucherid:
        if value['voucher_no'] not in voucher_no_list:
            voucher_no_list.append(value['voucher_no'])
            voucher_obj_distinct.append(value)
    suspense_order = SuspenseOrder.objects.values('voucher', 'session_id_id').\
    filter(purchase_order=id, is_cleared=1)
    request_status = request_notify()
    return render(request, 'voucher/voucher_show.html', {\
        'voucherid' : voucher_obj_distinct, 'suspense_order':suspense_order,\
        'request':request_status, 'message':message})


@login_required
def voucher_print(request):
    """
    This function displays a particular voucher
    Argument:Http Request
    Return:Render Voucher 
    """
    number = request.GET['voucher_no']
    session = request.GET['session']
    purchase_order_id = request.GET['purchase_order']
    flag = 0
    suspense_order = SuspenseOrder.objects.filter(voucher = number,
        purchase_order = purchase_order_id)
    if suspense_order:
        flag = 1
    calculatedistribution = CalculateDistribution.objects.\
    values('college_income_calculated', 'admin_charges_calculated',\
    'consultancy_asset', 'development_fund', 'total').\
    get(voucher_no = number, session = session)
    total_in_words = num2eng(calculatedistribution['total'])
    voucherid = VoucherId.objects.values('purchase_order', 'ratio',\
    'college_income', 'admin_charges', 'distribution__name',\
    'purchased_item__item__category__name',\
    'purchased_item__item__category__parent__parent',
    'purchased_item__item__category__parent').\
    filter(voucher_no = number, session = session)[0]
    purchase_order = voucherid['purchase_order']
    distribution = voucherid['distribution__name']
    ratio = voucherid['ratio']
    college_income = voucherid['college_income']
    admin_charges = voucherid['admin_charges']
    category_name = voucherid['purchased_item__item__category__name']
    lab_id = voucherid['purchased_item__item__category__parent__parent']
    lab_id_level_down = voucherid['purchased_item__item__category__parent']
    emp = Staff.objects.values('name','position__position').filter(lab=lab_id).\
    filter(always_included=1).order_by('position__rank','-seniority_credits')
    if emp:
        pass
    else:
        emp = Staff.objects.values('name','position__position').filter(
            lab=lab_id_level_down).filter(always_included=1).order_by(
            'position__rank','-seniority_credits')
    purchase_order_obj = PurchaseOrder.objects.\
    values('date_time', 'buyer','buyer__first_name','buyer__last_name',\
    'tds','buyer__customer__title','buyer__customer__company').\
    get(id = purchase_order)
    address = Customer.objects.values('address__street_address',\
    'address__district', 'address__pin', 'address__province').\
    get(user = purchase_order_obj['buyer'])
    date = purchase_order_obj['date_time']
    bill = Bill.objects.values('delivery_charges','total_cost',\
        'grand_total','amount_received','totalplusdelivery').\
    get(purchase_order = purchase_order_id)
    amount_received_inwords = num2eng(bill['amount_received'])
    taxes_applied = TaxesApplied.objects.values('surcharge__tax_name',\
        'surcharge__value','tax').filter(purchase_order = purchase_order_id)
    voucheridobj = VoucherId.objects.values('purchase_order_of_session',
        'purchase_order__mode_of_payment__method',
        'purchase_order__cheque_dd_number','purchase_order__cheque_dd_date',
        'purchase_order__mode_of_payment').\
    filter(purchase_order=purchase_order_id)[0]
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    if flag == 0:
        return render(request, 'voucher/voucher_report.html', {\
            'calculate_distribution' : calculatedistribution,\
            'admin_charges': admin_charges, 'college_income': college_income, \
            'ratio':ratio,'d_name': distribution,\
            'purchase_order': voucheridobj['purchase_order_of_session'],\
            'voucher':number, 'date': date,'address': address,\
            'buyer': purchase_order_obj, 'material': category_name,\
            'total_in_words': total_in_words, 'employee' : emp,\
             'header': header})
    else:
        return render(request, 'voucher/voucher_report_suspence.html',{
            'address':address, 'cost':bill, 'inwords':amount_received_inwords,\
            'date':date, 'suspense_voucher':number,\
            'job':voucheridobj['purchase_order_of_session'],\
            'tds':purchase_order_obj, 'tax':taxes_applied, 'header': header,\
            'material':category_name, 'buyer': purchase_order_obj,
            'method':voucheridobj['purchase_order__mode_of_payment__method'],
            'method_number':voucheridobj['purchase_order__cheque_dd_number'],
            'method_date':voucheridobj['purchase_order__cheque_dd_date'],
            'method_id':voucheridobj['purchase_order__mode_of_payment']})
