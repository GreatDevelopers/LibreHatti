"""
views for the useraccounts is described here
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

"""
this function displays the register and login button for user
"""
def register(request):
    """
    displays the form for items purchased
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/catalog/')
    else:
        form = UserCreationForm()
    """
    returns the login and signup option for user
    """
    return render(request, 'authentication/signup.html', { 'form': form,
                 })
 
