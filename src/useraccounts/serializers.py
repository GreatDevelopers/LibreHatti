# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Address, Customer, OrganisationType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("token", "username", "password")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "street_address", "district", "province", "nationality")


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationType
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "user_id",
            "address_id",
            "date_joined",
            "fax",
            "pan_no",
            "stc_no",
            "gst_in",
            "state",
            "state_code",
            "avatar",
            "tagline",
            "title",
            "is_org",
            "org_type_id",
            "company",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        data = self._kwargs["data"]
        address = Address.objects.filter(pk=data["address_id"]).values()
        organisation = OrganisationType.objects.filter(
            pk=data["org_type_id"]
        ).values()
        response["address"] = AddressSerializer(address[0]).data
        response["org_type"] = OrganisationSerializer(organisation[0]).data
        return response

    def create(self, validated_data):
        return validated_data
