from django.contrib import admin
from admin_app.models import Article, Subscriber, Website, MainMenu, SubMenu, ResourcesModel

admin.site.register(Article)
admin.site.register(Subscriber)
admin.site.register(Website)
admin.site.register(MainMenu)
admin.site.register(SubMenu)
admin.site.register(ResourcesModel)