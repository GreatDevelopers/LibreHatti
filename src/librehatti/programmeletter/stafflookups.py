from django.db.models import Q

from django.utils.html import escape

from librehatti.suspense.models import Staff

from ajax_select import LookupChannel

class StaffLookup(LookupChannel):
    """
    This class suggests staff names (Ajax Effect) while selecting staff 
    in programme letter
    """

    model = Staff

    def get_query(self, q, request):
        staff = Staff.objects.all()
        for value in q.split():
            staff = staff.filter(Q(name__icontains=value)| \
                Q(code__icontains=value) \
                |Q(department__title__icontains=value)\
                |Q(position__position__icontains=value))
        return staff[0:15]

    def get_result(self, obj):
        return str(obj.name)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        result = Staff.objects.values('name','code',
            'department__title','position__position').filter(id = obj.id)[0]
        return "<b>Name:</b> %s <br> <b>Position:</b> %s <br> <b>department:</b> %s \
        <br> <b>Code:</b> %s <hr>" %((result['name'], result['position__position'],
            result['department__title'], result['code']))
