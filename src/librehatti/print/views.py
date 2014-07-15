from django.shortcuts import render
from librehatti.catalog.models import Category, Product, PurchaseOrder,PurchasedItem
from django.db.models import Sum
from django.http import HttpResponse
    
def lab_report(request):
    if request.method == 'POST':
        material = request.POST['material']
        start_date = request.POST['From']
        end_date = request.POST['To']
        
        
        purchase_item= PurchasedItem.objects.filter(purchase_order__date_time__range
                  =(start_date,end_date),item__name=material).values( 
                    'purchase_order_id','purchase_order__date_time',
                   'purchase_order__buyer_id__username',
                  'purchase_order__buyer_id__customer__title',
                  'purchase_order__buyer_id__customer__company','price',
                  'purchase_order__buyer_id__customer__is_org')
    
        total=PurchasedItem.objects.filter(purchase_order__date_time__range 
        =(start_date,end_date)).aggregate(Sum('price')).get('price__sum', 0.00)
        return render(request, 'print/lab_reports.html', { 'purchase_item':
          purchase_item,'start_date':start_date,'end_date':end_date,'total_cost':total})
    else:     
        lab_info=Category.objects.all()
        return render(request, 'print/form.html',{'lab_info':lab_info})
        if request.method == 'POST':
            lab = request.POST['Lab']
            test_info = Category.objects.filter(category__parent=lab)
            return render(request, 'print/form.html',{ 'test_info':test_info})
        if request.method == 'POST':
            test = request.POST['Test'] 
            material_info = Product.objects.filter(category__name=test)
            return render(request, 'print/form.html',{ 'material_info':material_info})