# -*- coding: utf-8 -*-
from django.contrib.auth.admin import admin
from librehatti.reports.models import SavedRegisters


admin.autodiscover()

admin.site.register(SavedRegisters)
