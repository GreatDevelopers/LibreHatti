from django.urls import re_path

from librehatti.bills import views


urlpatterns = [
        re_path(r'^quoted_bill_cal/',views.quoted_bill_cal, name= 'quoted_bill_cal'),
        re_path(r'^quoted_order_added_success/',views.quoted_order_added_success, name= 'quoted_order_added_success'),
        re_path(r'^select_note/',views.select_note, name= 'select_note'),
        re_path(r'^select_note_save/',views.select_note_save, name= 'select_note_save'),
        re_path(r'^new_note_line/',views.new_note_line, name= 'new_note_line'),
        re_path(r'^delete_note/',views.delete_note, name= 'delete_note'),
        re_path(r'^quoted_order_of_session/',views.quoted_order_of_session, name= 'quoted_order_of_session')
]
