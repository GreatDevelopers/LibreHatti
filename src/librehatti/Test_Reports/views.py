from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from librehatti.settings import TEMPLATE_DIRS
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.core.files import File
from librehatti.Test_Reports.models import *
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
    report_get_id = Test_Reports.objects.values('id','mix').get(Session_id=data_session['Session'], Voucher = data_session['Voucher']) 
    count = 1
    report_content = '' 
    date_format = data_session['Refernce_Date'].split("-")
    date_format_new = date_format[2] + "/" + date_format[1] + "/" + date_format[0]
    date_format_for_test = data_session['Testing_Date'].split("-")
    date_format_new_for_test = date_format_for_test[2] + "/" + date_format_for_test[1] + "/" + date_format_for_test[0]
    filename = "trial_copy.tex"
    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial.tex'))
    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_copy.tex'))
    if request.method == 'POST':
        r = request.POST['header']
    else:
        return render(request,"Test_Reports/index.html",{'r':''})
 
    for des in  Test_Report_Descriptions.objects.filter(report_id_id = report_get_id['id']):

            date_format_for_start = unicode(des.Start_Date).split("-")
            date_format_new_for_start = date_format_for_start[2] + "/" + date_format_for_start[1] + "/" + date_format_for_start[0]
            
            if report_get_id['mix'] == 1:
                report_content += str(count) + "&" + des.Description + "&" + date_format_new_for_start + "&" + des.mix + "&" + des.Strength + "\\" + "\\" + "\hline"
                if request.POST['header'] == 'yes':
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_copy.tex'))
                    filename = "trial_copy.pdf"
                else:
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_latex_tamplate.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_latex_tamplate_copy.tex'))
                    filename = "my_latex_tamplate_copy.pdf"
                
            else:
                report_content += str(count) + "&" + des.Description + "&" + date_format_new_for_start + "&" + des.Strength + "\\" + "\\" + "\hline"
                if request.POST['header'] == 'no':                                                    
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_tamplate_without_mix.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/my_tamplate_without_mix_copy.tex'))
                    filename = "my_tamplate_without_mix_copy.pdf"
                else:                                
                    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_without_mix.tex'))
                    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/trial_without_mix_copy.tex'))
                    filename = "trial_without_mix_copy.pdf"

    count += 1               
    if r == 'yes':
        f = open(texfilename,'r+')
        data = f.read()
        f.close()
        fw = open(texfilename_copy,'w+')
        fw.write(data)
        fw.close()
        texfile = os.open(texfilename_copy, os.O_RDWR)
        os.write(texfile, render_to_string(texfilename_copy, {'address': data_session['Client'].replace('&','\&'),
								 	'address2': data_session['Address'].replace('&','\&'),
								 	'address3': data_session['City'].replace('&','\&'),
									'sub': data_session['Subject'].replace('&','\&'),
									'ref_no': data_session['Refernce_no'],
									'ref_date': data_session['Refernce_Date'].replace('-','/'),
									'start_date': data_session['Refernce_Date'].replace('-','/'),
                                    'table': report_content,    
									'test_date': date_format_new,
									'ref_date': date_format_new_for_test,
									'start_date': date_format_new_for_test,
                                    'table': report_content,    
									'test_date': date_format_new,
									'ref_date': date_format_new_for_test,
									'start_date': date_format_new_for_test,
                                                                        'table': report_content,    
									}))
        os.close(texfile)
        call(['sh',os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/shell.sh'))])  
 
    if r == 'no':
        f = open(texfilename,'r+')
        data = f.read()
        f.close()
        fw = open(texfilename_copy,'w+')
        fw.write(data)
        fw.close()
        texfile = os.open(texfilename_copy,os.O_RDWR)
        os.write(texfile, render_to_string(texfilename_copy,{'address': data_session['Client'].replace('&','\&'),
									'address2': data_session['Address'].replace('&','\&'),
								 	'address3': data_session['City'].replace('&','\&'),
									'sub': data_session['Subject'].replace('&','\&'),
									'ref_no': data_session['Refernce_no'],
									'ref_date': data_session['Refernce_Date'].replace('-','/'),
									'start_date': data_session['Refernce_Date'].replace('-','/'),
                                    'table': report_content,    
									'test_date': date_format_new,
									'ref_date': date_format_new_for_test,
									'start_date': date_format_new_for_test,
                                    'table': report_content,    
									'test_date': date_format_new,
									'ref_date': date_format_new_for_test,
									'start_date': date_format_new_for_test,
                                                                        'table': report_content,    
									}))
        os.close(texfile)
    call(['sh',os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/shell.sh'))])   
    return render(request,"Test_Reports/index.html",{'r':'/'+filename,'res': request.POST['header']})

@login_required
def Soil_building_report(request):
    data_session = request.session.get('data')
    filename = "soil_building_copy.pdf"
    texfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/soil12.tex'))
    texfilename_copy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/soil_building_copy.tex'))
    report_get_id = Soil_building.objects.values('id').get(Session_id=data_session['Session'], Voucher = data_session['Voucher'])  	 
    report_content = '' 
    count = 1
    for des in  Soil_building_des.objects.filter(report_id_id = report_get_id['id']):
        report_content += str(count) + "&" + des.Dt + "&" + des.Ob_Pr + "&" + des.Corr_F + "&" + des.Ob_N_V + "&" + des.Corr_N_V + "\\" + "\\" + "\hline"
        count +=1        
    f = open(texfilename,'r+')
    data = f.read()
    f.close()
    fw = open(texfilename_copy,'w+')
    fw.write(data)
    fw.close()
    texfile = os.open(texfilename_copy,os.O_RDWR)
    os.write(texfile, render_to_string(texfilename_copy,{'title': data_session['Site_Name'].replace('&','\&'),
	                    			'dateoftest': data_session['Date_of_Testing'].replace('&','\&'),
								 	'strtype': data_session['Type_of_str'].replace('&','\&'),
									'lati': data_session['Latitude_N'].replace('&','\&'),
									'logitude': data_session['Longitude_E'],
									'p1': data_session['Presence_1'],
									'p2': data_session['Presence_2'],
                                    's1':data_session['Submitted_1'],    
									's2': data_session['Submitted_2'],
									's3': data_session['Submitted_3'],
                                    'bore':data_session['Bore_Hole'],
									'sitename': data_session['Site_Name'],
                                    'watertable': data_session['Water_Table'],    
									'walldt': data_session['Wall_Dt'],
									'wallb': data_session['Wall_B'],
									'coldf': data_session['Col_Df'],
                                    'coll': data_session['Col_L'],
                                    'colb':data_session['Col_B'],
                                    'gamawall':data_session['Gama_wall'],
                                    'wallc':data_session['Wall_C'],
                                    'wallphey':data_session['Wall_Phay'],
                                    'wallpheyfe':data_session['Wall_Phay_Fe'],
                                    'wallnc':data_session['Wall_Nc'],
                                    'wallnq':data_session['Wall_Nq'],
                                    'wallny':data_session['Wall_Ny'],
                                    'wallsc':data_session['Wall_Sc'],
                                    'wallsq':data_session['Wall_Sq'],
                                    'wallsy':data_session['Wall_Sy'],
                                    'walldc':data_session['Wall_dc'],
                                    'walldqdy':data_session['Wall_dq_dy'],
                                    'wallw':data_session['Wall_w'],
                                    'wallpeq':data_session['Wall_peq'],
                                    'walltotal':data_session['Wall_Total'],
                                    'wallt2':data_session['Wall_T_2'],
                                    'colsc' :data_session['Col_Sc'],
                                    'colsq':data_session['Col_Sq'],                     
                                    'colsy':data_session['Col_Sy'],
                                    'coldc':data_session['Col_dc'],
                                    'coldqdy':data_session['Col_dq_dy'],
                                    'colpeq':data_session['Col_peq'],
                                    'coltotal':data_session['Col_Total'],
                                    'colt2':data_session['Col_T_2'],
                                    'wallnv':data_session['Wall_N_V'],
                                    'walls':data_session['Wall_S'],
                                    'wallvalue':data_session['Wall_Value'],
                                    'wallnetv':data_session['Wall_Net_V'],
                                    'wallgv':data_session['Wall_G_V'],
                                    'colnv':data_session['Col_N_V'],
                                    'colvalue':data_session['Col_Value'],
                                    'colnetv':data_session['Col_Net_V'],
                                    'colgv':data_session['Col_G_V'],
                                    'table':report_content,
									}))
    os.close(texfile)
    call(['sh',os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates/Test_Reports/shell.sh'))])   
    return render(request,"Test_Reports/soil.html",{"r":"/"+filename})
