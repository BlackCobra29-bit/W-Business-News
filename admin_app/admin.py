from django.contrib import admin
from admin_app.models import Article, Subscriber, Website, ResourcesModel
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Subscriber)
admin.site.register(Website)
admin.site.register(ResourcesModel)

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)