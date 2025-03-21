from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from admin_app.models import Article

class UserIndex(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')
        
        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)
        
        context["articles"] = articles
        return context
