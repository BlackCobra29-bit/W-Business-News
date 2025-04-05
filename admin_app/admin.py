from django.contrib import admin
from admin_app.models import Article, Subscriber, Website, ResourcesModel

admin.site.register(Article)
admin.site.register(Subscriber)
admin.site.register(Website)
admin.site.register(ResourcesModel)