from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.models import User
from ajax_select import LookupChannel

class BuyerLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return User.objects.values('first_name','last_name',
            'customer__title','customer__address__street_address',
            'customer__address__city').filter(Q(username__icontains=q)| \
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | \
            Q(customer__address__street_address__icontains=q) | \
            Q(customer__address__city__icontains=q)).filter(~Q(id = 1)).\
            select_related('customer')[:10]

    def get_result(self, obj):
        return "%s" % (str(obj['first_name'] + ' ' + obj['last_name'] + ' ' + \
            obj['customer__title']))

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        #self.response_query = str(obj.first_name + ' ' + obj.last_name)
        return "<b>Name or Title:</b> %s <br> <b>Address:</b> %s <br> %s <hr>" % \
            (str(obj['first_name'] + ' ' + obj['last_name'] + ' ' + obj['customer__title']), \
            str(obj['customer__address__street_address']), (obj['customer__address__city']))
