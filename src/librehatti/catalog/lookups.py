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
        self.response_query = str(obj.first_name + ' ' + obj.last_name)
        return "%s" % (escape(self.response_query))
