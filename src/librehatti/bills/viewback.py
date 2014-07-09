def confirm(request,client_id):
    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values('quote_item__name', 'quote_qty')
    i_d = quoted_order.quote_buyer_id_id
    form = ConfirmForm(initial={'quote_item':'item1', 'qty1':'quote_qty'})
    return render(request, 'bills/confform.html', {'quoted_order' : quoted_order,'form':form,
                 'quoted_item' : quoted_item,  'id' : i_d})



def final(request,name):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quote_qty = request.POST ["quote_qty"]
            quote_item = request.POST ["quote_item"]
            obj = PurchasedItem(qty = quote_qty)
            obj.item = Product(name = quote_item)
            obj.purchase_order= PurchaseOrder.objects.get(id=1)
          
            obj.save()
            return HttpResponse('quote')
            #return HttpResponse('quote_qty')
            #obj = PurchasedItem(qty=quote_qty)
            #obj.item= PurchasedItem.objects.get(item__name=quote_item)
            #obj.purchase_order= PurchaseOrder.objects.get(id=client_id)
            #obj.save()
            #quoted_item = PurchasedItem.objects.filter(client_id=buyer_id).values( 'item__name','qty')
            
            return render(request, 'bills/bills.html',  {'quoted_item':quoted_item})

    else:
             client_id = 1
             quoted_order = QuotedOrder.objects.get(pk=int(client_id))
             quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
             total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
             i_d = quoted_order.quote_buyer_id_id
             form = ConfirmForm()
             return render(request, 'bills/bills.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d,'form':form})
      

         
         #return render(request, 'bills/bills.html',{'form':form})
     

