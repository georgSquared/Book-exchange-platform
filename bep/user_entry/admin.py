from django.contrib import admin
from user_entry.models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'first_name', 'last_name', 'points', 'books_available', 'books_borrowed', 'address')

admin.site.register(UserProfile, UserProfileAdmin)