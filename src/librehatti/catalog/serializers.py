# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import FinancialSession


class FinancialSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSession
        fields = ("session_start_date", "session_end_date")
