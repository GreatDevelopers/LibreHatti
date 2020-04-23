from django.db.models import Q

from django.utils.html import escape

from django.contrib.auth.models import User

from ajax_select import LookupChannel


class BuyerLookup(LookupChannel):
    """
    This class suggests user names (AJAX Effect) while filling client name for a purchase order
    """

    model = User

    def get_query(self, q, request):
        user = User.objects.all()
        for value in q.split():
            user = user.filter(
                Q(username__icontains=value)
                | Q(first_name__icontains=value)
                | Q(last_name__icontains=value)
                | Q(customer__address__street_address__icontains=value)
                | Q(customer__address__district__icontains=value)
                | Q(customer__address__province__icontains=value)
                | Q(customer__title__icontains=value)
                | Q(customer__company__icontains=value)
                | Q(customer__gst_in__icontains=value)
                | Q(customer__telephone__icontains=value)
            )
        return user[0:15]

    def get_result(self, obj):
        return str(obj.username)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        result = User.objects.values(
            "first_name",
            "last_name",
            "customer__title",
            "customer__address__street_address",
            "customer__address__district",
            "customer__company",
            "customer__gst_in",
            "customer__telephone",
        ).filter(id=obj.id)[0]
        return (
            "<b>Name or Title:</b> %s <br> <b>Company:</b> %s <br> <b>Address:</b> %s <br> %s <br> <b>GST No:</b> %s <br> <b>Phone:</b> %s \
        <hr>"
            % (
                (
                    result["first_name"]
                    + " "
                    + result["last_name"]
                    + " "
                    + result["customer__title"]
                ),
                (result["customer__company"]),
                (result["customer__address__street_address"]),
                (result["customer__address__district"]),
                (result["customer__gst_in"]),
                (result["customer__telephone"]),
            )
        )
