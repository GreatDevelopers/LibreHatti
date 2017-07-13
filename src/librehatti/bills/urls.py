from django.conf.urls import url, patterns

urlpatterns = patterns('librehatti.bills.views',
                       url(r'^quoted_bill_cal/', 'quoted_bill_cal'),
                       url(r'^quoted_order_added_success/',
                           'quoted_order_added_success'),
                       url(r'^select_note/', 'select_note'),
                       url(r'^select_note_save/', 'select_note_save'),
                       url(r'^new_note_line/', 'new_note_line'),
                       url(r'^delete_note/', 'delete_note'),
                       url(r'^quoted_order_of_session/',
                           'quoted_order_of_session')
                       )
