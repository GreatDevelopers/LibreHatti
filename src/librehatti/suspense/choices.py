from librehatti.catalog.models import PurchaseOrder

purchase_ids=[]
a = PurchaseOrder.objects.all()
	
for i in a:
	if i.is_suspense==True:
		purchase_ids.append((i.id,i.id))
suspense_ids=tuple(purchase_ids)
CHOICES=suspense_ids
