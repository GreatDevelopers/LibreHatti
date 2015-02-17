from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from librehatti.Test_Reports.models import *
from librehatti.settings import TEMPLATE_DIRS
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.core.files import File
from django.template.loader import render_to_string
from librehatti.voucher.models import VoucherId, Distribution
from librehatti.voucher.models import FinancialSession, CalculateDistribution
from librehatti.voucher.models import VoucherTotal
from librehatti.suspense.models import *
from useraccounts.models import *
from librehatti.catalog.models import *
import os
from subprocess import call
from .forms import Test_Reports

@login_required
def Test_Reports_data(request):
    session = request.GET['session']
    voucher = request.GET['voucher']
    session_id = VoucherId.objects.values('purchased_item_id','purchase_order_id','purchase_order_of_session').get(session_id=session, voucher_no=voucher)
    purchased_item = PurchasedItem.objects.values('item_id').get(id=session_id['purchased_item_id'])
    product = Product.objects.values('name').get(id=purchased_item['item_id'])    
    purchase_order = PurchaseOrder.objects.values('buyer_id','reference_date').get(id=session_id['purchase_order_id'])
    buyer_id = User.objects.values('first_name','last_name','id').get(id=purchase_order['buyer_id'])
    address_id = Customer.objects.values('address_id').get(user=buyer_id['id'])
    street_address = Address.objects.values('street_address','city').get(id=address_id['address_id'])
    Testing_date = SuspenseClearance.objects.values('test_date').get(id=session)
     
    data =buyer_id['first_name']+":"+buyer_id['last_name']+":"+street_address['street_address']+":"+unicode(session_id['purchase_order_of_session'])+":"+Testing_date['test_date']+":"+product['name']+":"+street_address['city']
    if buyer_id['first_name'] is not None:
        return HttpResponse(data)
    else:
        return HttpResponse('fail')

@login_required
def Reports(request):
    data_session = request.session.get('data')
    report_get_id = Test_Reports.objects.values('id','mix').get(Session_id = data_session['Session'], Voucher = data_session['Voucher']) 
    count = 1
    filename = "trial_copy.tex"
    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial.tex'))
    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_copy.tex'))
    if request.method == 'POST':
        r = request.POST['header']
    else:
        return render(request,"Test_Reports/index.html",{'r':''})

    for des in  Test_Report_Descriptions.objects.filter(report_id_id = report_get_id['id']):
            report_content=''
            if report_get_id['mix'] == 1:
                report_content += str(count) +"&"+des.Description+"&"+unicode(des.Start_Date)+"&"+des.mix+"&"+des.Strength+"\\"+"\\"+"\hline"
                if request.POST['header'] == 'yes':
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_copy.tex'))
                else:
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_latex_tamplate.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_latex_tamplate_copy.tex'))
                

            else:
                report_content += str(count)+"&"+des.Description+"&"+unicode(des.Start_Date)+"&"+des.Strength+"\\"+"\\"+"\hline"
                if request.POST['header'] == 'no':                                                    
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_tamplate_without_mix.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_tamplate_without_mix_copy.tex'))
                else:                                
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_without_mix.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_without_mix_copy.tex'))


    count += 1               
    if r == 'yes':
        f = open(texfilename ,'r+')
        data = f.read()
        f.close()
        fw = open(texfilename_copy, 'w+')
        fw.write(data)
        fw.close()
        texfile = os.open(texfilename_copy, os.O_RDWR)
        os.write(texfile, render_to_string(texfilename_copy, {'address': data_session['Client'].replace('&','\&'),
								 	'address2': data_session['Address'].replace('&','\&'),
								 	'address3': data_session['City'].replace('&','\&'),
									'sub': data_session['Subject'].replace('&','\&'),
									'ref_no': data_session['Refernce_no'],
									'ref_date': data_session['Refernce_Date'],
									'start_date': data_session['Refernce_Date'],
                                    'table': report_content,    
									}))
        os.close(texfile)
        call(['sh',os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/shell.sh'))])   
    if r == 'no':
        f = open(texfilename ,'r+')
        data = f.read()
        f.close()
        fw = open(texfilename_copy, 'w+')
        fw.write(data)
        fw.close()
        texfile = os.open(texfilename_copy, os.O_RDWR)
        os.write(texfile, render_to_string(texfilename_copy, {'address': data_session['Client'].replace('&','\&'),
									'address2': data_session['Address'].replace('&','\&'),
								 	'address3': data_session['City'].replace('&','\&'),
									'sub': data_session['Subject'].replace('&','\&'),
									'ref_no': data_session['Refernce_no'],
									'ref_date': data_session['Refernce_Date'],
									'start_date': data_session['Refernce_Date'],
                                    'table': report_content,    
									}))
        os.close(texfile)
        call(['sh',os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/shell.sh'))])   
    return render(request,"Test_Reports/index.html",{'r':report_content})
