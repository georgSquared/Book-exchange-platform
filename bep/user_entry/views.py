from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from user_entry.forms import UserProfileForm
from user_entry.models import UserProfile
from user_entry.models import User
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
import urllib
import urllib2
from xml.dom import minidom
from books.models import Book

# Create your views here.

class UserProfileDetail(DetailView):
    model = UserProfile
    success_url = reverse_lazy('userprofile_detail')


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ("first_name", "last_name", "address")
    success_url = "/"


def confirmdelete(request):

    return render_to_response("user_entry/confirm_delete.html", context_instance=RequestContext(request))

def delete(request):
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.delete()
        return render_to_response("user_entry/delete.html", context_instance=RequestContext(request))


def index(request):
    if request.user.is_authenticated():
        bookresults = Book.objects.filter(owner=request.user)
        borrowedbooks = Book.objects.filter(borrower=request.user)
        user = User.objects.get(username=request.user)
        profile = user.profile
        if profile.first_name == "":
            profile.first_name=request.user.first_name
            profile.last_name=request.user.last_name
            profile.address=""
            profile.save()
        return render_to_response("user_entry/index.html",{'results': bookresults, 'results2': borrowedbooks}, context_instance=RequestContext(request))

    return render_to_response("user_entry/index.html", context_instance=RequestContext(request))

def get_name(request):
    
    if request.method == 'POST':
        
        form = UserProfileForm(request.POST, instance=request.user.getprofile())

        if form.is_valid():
            profile = form.save(commit=True)
            profile.first_name = first_name

            return HttpResponseRedirect("user_entry/index.html")


    else:
        form = UserProfileForm()

    return render(request, 'user_entry/name.html', {'form': form}, context_instance=RequestContext(request))
