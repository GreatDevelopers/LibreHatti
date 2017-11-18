from django.http import HttpResponse
from librehatti.catalog.request_change import request_notify
from .forms import DispatchForm
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect

def dispatch_view(request):
    """
    This view allows user to view DispatchForm. If request.method==POST
    then it will save the values of the field otherwise display form.
    """
    if request.method == "POST":

        form = DispatchForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = DispatchForm()
    return render(request, 'dispatch_register/add_entry.html', {'form': form})

