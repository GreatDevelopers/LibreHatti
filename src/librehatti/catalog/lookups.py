from django.db.models import Q

from django.utils.html import escape

from django.contrib.auth.models import User

from ajax_select import LookupChannel

class BuyerLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        user = User.objects.all()
        for value in q.split():
            user = user.filter(Q(username__icontains=value)| \
                Q(first_name__icontains=value) \
                | Q(last_name__icontains=value) \
                |Q(customer__address__street_address__icontains=value)\
                |Q(customer__address__city__icontains=value)\
                |Q(customer__address__province__icontains=value)
                |Q(customer__title__icontains=value))
        return user[0:15]

    def get_result(self, obj):
        return unicode(obj.username)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        result = User.objects.values('first_name','last_name',
            'customer__title','customer__address__street_address',
            'customer__address__city').filter(id = obj.id)[0]
        return "<b>Name or Title:</b> %s <br> <b>Address:</b> %s <br> %s \
        <hr>" %((result['first_name'] + ' ' + result['last_name'] + ' ' + \
            result['customer__title']), \
            (result['customer__address__street_address']), \
            (result['customer__address__city']))
