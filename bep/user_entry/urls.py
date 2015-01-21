from django.conf.urls import patterns, url
from user_entry import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
     url(r'^get_name/', views.get_name, name='get_name'),
     url(r'^detail/(?P<pk>\d+)$', views.UserProfileDetail.as_view(), name='userprofile_detail'),
     url(r'^edit/(?P<pk>\d+)$', views.UserProfileUpdate.as_view(), name='userprofile_edit'),
     url(r'^confirm_delete/', views.confirmdelete, name='confirm_delete'),
     url(r'^delete/', views.delete, name='delete'),
     
    
)
