from django.conf.urls import patterns, url
from books import views

urlpatterns = patterns('',
	url(r'^search/' ,views.search , name='search'),
	url(r'^add/' ,views.add , name='add'),
	url(r'^find/' ,views.find , name='find'),
    url(r'^makeavailable/' ,views.makeavailable , name='makeavailable'),
    url(r'^selectuser/' ,views.selectuser , name='selectuser'),
    url(r'^cancelreservation/' ,views.cancelreservation , name='cancelreservation'), 
    url(r'^approve/' ,views.approve , name='approve'), 
)
