# -*- coding: utf-8 -*-
"""
views for the useraccounts is described here
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import (
    CustomerSerializer,
    UserSerializer,
    UserSerializerWithToken,
)


@api_view(["GET"])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        data = Customer.objects.filter(pk=1).values()
        serializer = CustomerSerializer(data=data[0])
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        data = request.data
        user_data = data.pop("user")
        user = User.objects.create_user(
            user_data["username"], user_data["email"], "testing123"
        )
        data["user"] = user.pk
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CustomerSearch(APIView):
    def get(self, request):
        data = Customer.objects.filter(pk=1).values()
        serializer = CustomerSerializer(data=data[0])
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        print(request.data)
        return Response("")


def register(request):
    """
    displays the form for items purchased
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/catalog/")
    else:
        form = UserCreationForm()
    """
    returns the login and signup option for user
    """
    return render(request, "authentication/signup.html", {"form": form})
