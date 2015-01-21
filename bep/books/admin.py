from django.contrib import admin
from books.models import Book

class BookAdmin(admin.ModelAdmin):
	list_display = ('owner', 'title', 'image_url', 'author', 'available','borrower','permission')

admin.site.register(Book, BookAdmin)
