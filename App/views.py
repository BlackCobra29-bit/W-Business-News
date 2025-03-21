from django.shortcuts import render
from admin_app.models import Article
from django.views.generic import TemplateView

class UserIndex(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.order_by("-created_at")
        return context