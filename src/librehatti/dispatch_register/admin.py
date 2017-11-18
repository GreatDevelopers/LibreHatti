from django.contrib import admin
from .models import DispatchEntry
from .models import SubjectsChoice, RemarksChoice
from .forms import DispatchForm, SubjectsForm, RemarksForm
from ajax_select.admin import AjaxSelectAdmin

admin.autodiscover()

class SubjectsChoicesAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete the subject choices
    """
    form = SubjectsForm
    model = SubjectsChoice

class RemarksChoicesAdmin(admin.ModelAdmin):
    """
    This class is used to add, edit or delete the remark choices
    """
    form = RemarksForm
    model = RemarksChoice

class DispatchEntryAdmin(AjaxSelectAdmin):
    """
    This class is used to add, edit or delete the dispatch entry.
    """
    form = DispatchForm
    list_display = ('dispatch_no','date','name_of_Dept_or_Client',\
    'agency', 'subjects_select', 'remarks_select')
    search_fields = ['=name_of_Dept_or_Client','=address']
    list_filter = ['dispatch_no', 'name_of_Dept_or_Client']
    list_per_page = 20

    """
    This function will override the value of Subjects field in
    list_display key. It is used to display the multiple selected
    subjects separated by comma delimiter.
    """

    def subjects_select(self, obj):
        return ", ".join([subject.subject_name for subject \
        in obj.subjects.all()])
        #here subjects is the column of model DispatchEntry

    """
    Just like Subjects function it will display the value of remarks.
    """

    def remarks_select(self, obj):
        return ", ".join([remark.remark_name for remark \
        in obj.remarks.all()])

admin.site.register(SubjectsChoice, SubjectsChoicesAdmin)
admin.site.register(DispatchEntry, DispatchEntryAdmin)
admin.site.register(RemarksChoice, RemarksChoicesAdmin)
