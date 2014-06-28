from django.shortcuts import render
from librehatti.catalog.models import Category, PurchaseOrder,PurchasedItem
from django.db.models import Sum

def add_material(request):
  if request.method == 'POST':
    material = request.POST['material']
    start_date = request.POST['From']
    end_date = request.POST['To']
    purchase_item= PurchasedItem.objects.filter(purchase_order__date_time__range
                  =(start_date,end_date)).filter(item__category__name=material).values_list( 
                    'purchase_order_id','purchase_order__date_time',
                   'purchase_order__buyer_id__username',
                  'purchase_order__buyer_id__customer__title','price')
    total=PurchasedItem.objects.filter(purchase_order__date_time__range 
        =(start_date,end_date)).aggregate(Sum('price')).get('price__sum', 0.00)
    return render(request, 'print/lab_reports.html', { 'purchase_item':purchase_item,
                 'start_date':start_date,'end_date':end_date,'total_cost':total})
  else:     
    material_name = Category.objects.values('name')
    return render(request,'print/form.html',{'material_name': material_name})    
    