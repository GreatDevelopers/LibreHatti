from django.conf.urls import url, patterns 

urlpatterns = patterns('librehatti.print.views',
        url(r'^addmaterial/', 'add_material'),

)
