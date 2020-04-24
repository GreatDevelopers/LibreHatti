# -*- coding: utf-8 -*-
"""
views for the useraccounts is described here
"""
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


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
