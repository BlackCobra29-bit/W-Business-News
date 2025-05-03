from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django_summernote.models import Attachment

admin.site.site_header = "Wahid Business News"
admin.site.site_title = "Wahid Business News"
admin.site.index_title = "Welcome to Wahid Business News"

User._meta.verbose_name = "System Admin"
User._meta.verbose_name_plural = "System Admins"

for model in apps.get_models():
    if model != User:
        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

try:
    admin.site.unregister(Attachment)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass