from django.contrib import admin

# Register your models here.
from .models import User, Book, Chat, Feedback

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Chat)
admin.site.register(Feedback)
