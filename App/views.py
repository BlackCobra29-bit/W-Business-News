from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from admin_app.models import Article
from admin_app.models import Subscriber
from admin_app.models import Website
from hitcount.views import HitCountMixin
from hitcount.models import HitCount


class UserIndex(TemplateView):
    template_name = "index.html"
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
        Subscriber.objects.create(email=email)
        return JsonResponse({'success': True, 'message': 'You have successfully subscribed to our newsletter.'})

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 3)
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
    template_name = "page-specfic.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Diesel Vehicle").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 1)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)
        context["articles"] = articles
        return context

class Electricvehicles(TemplateView):
    template_name = "page-specfic.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_list = Article.objects.filter(news_type="Electric Vehicle").only('id', 'title', 'content', 'created_at').order_by("-created_at")
        paginator = Paginator(article_list, 1)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)
        context["articles"] = articles
        return context

class BanksFinancial(TemplateView):
    template_name = "page-specfic.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

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
    template_name = "page-specfic.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

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