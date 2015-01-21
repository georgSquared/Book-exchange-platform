from django.forms import ModelForm
from django import forms
from user_entry.models import UserProfile



class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name')
