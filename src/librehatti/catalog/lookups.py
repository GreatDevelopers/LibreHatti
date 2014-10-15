from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.models import User
from ajax_select import LookupChannel

class BuyerLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return User.objects.filter(Q(username__icontains=q)| \
        	Q(first_name__icontains=q) | Q(last_name__icontains=q)).\
               filter(~Q(id = 1)).select_related('customer')

    def get_result(self, obj):
        return unicode(obj.username)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        result = User.objects.values('first_name','last_name',
            'customer__title','customer__address__street_address',
            'customer__address__city').filter(id = obj.id)[0]
        return "<b>Name or Title:</b> %s <br> <b>Address:</b> %s <br> %s <hr>" % \
            ((result['first_name'] + ' ' + result['last_name'] + ' ' + \
            result['customer__title']), \
            (result['customer__address__street_address']), \
            (result['customer__address__city']))
