from django.conf.urls import url

from librehatti.bills import views


urlpatterns = [
        url(r'^quoted_bill_cal/',views.quoted_bill_cal, name= 'quoted_bill_cal'),
        url(r'^quoted_order_added_success/',views.quoted_order_added_success, name= 'quoted_order_added_success'),
        url(r'^select_note/',views.select_note, name= 'select_note'),
        url(r'^select_note_save/',views.select_note_save, name= 'select_note_save'),
        url(r'^new_note_line/',views.new_note_line, name= 'new_note_line'),
        url(r'^delete_note/',views.delete_note, name= 'delete_note'),
        url(r'^quoted_order_of_session/',views.quoted_order_of_session, name= 'quoted_order_of_session')
]
