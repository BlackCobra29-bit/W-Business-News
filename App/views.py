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

        old_articles = Article.objects.only('id', 'title').order_by("created_at")[:5]

        context["articles"] = articles
        context["old_articles"] = old_articles
        return context

    
class Dieselvehicles(TemplateView):
    template_name = "diesel_vehicles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Diesel Vehicle").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)

        context["articles"] = articles
        return context
    
class Electricvehicles(TemplateView):
    template_name = "electric_vehicle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Electric Vehicle").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)

        context["articles"] = articles
        return context
    
class BanksFinancial(TemplateView):
    template_name = "electric_vehicle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Banks & Financial").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)

        context["articles"] = articles
        return context
    
class LogisticsTransport(TemplateView):
    template_name = "electric_vehicle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Logistics and Transport").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 4)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)

        context["articles"] = articles
        return context