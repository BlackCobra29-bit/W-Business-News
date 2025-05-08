from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Prefetch
from admin_app.models import Article, ResourcesModel
from admin_app.models import Subscriber
from admin_app.models import Comment
from admin_app.models import Website
from hitcount.views import HitCountMixin
from hitcount.models import HitCount

# Define a mapping for slugified versions
NEWS_TYPE_SLUG_MAP = {
    'trucks-diesel-vehicle': 'trucks_diesel',
    'machineries-diesel-vehicle': 'machineries_diesel',
    'cars-diesel-vehicle': 'cars_diesel',
    'electric-vehicle': 'electric_vehicle',
    'news-banks-financial': 'news_banks_financial',
    'regulations-banks-financial': 'regulations_banks_financial',
    'news-logistics-transport': 'news_logistics_transport',
    'regulations-logistics-transport': 'regulations_logistics_transport',
}

class UserIndex(HitCountMixin, TemplateView):
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

        article_list = Article.objects.only('id', 'slug', 'title', 'content', 'created_at')\
                .prefetch_related(Prefetch(
                    'comments',
                    queryset=Comment.objects.filter(approved=True).only('id', 'article', 'name', 'email', 'content', 'created_at')
                ))\
                .order_by("-created_at")

        paginator = Paginator(article_list, 15)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            articles = paginator.page(1)

        old_articles = Article.objects.only('id', 'title').order_by("created_at")[:5]

        context["articles"] = articles
        context["old_articles"] = old_articles
        return context

class NewsByCategoryView(HitCountMixin, TemplateView):
    template_name = 'page-specfic.html'

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['news_type']
        internal_news_type = NEWS_TYPE_SLUG_MAP.get(slug)

        if internal_news_type is None:
            context['business_articles'] = []
            return context

        business_articles = Article.objects.filter(news_type=internal_news_type) \
            .only('id', 'slug', 'title', 'content', 'created_at') \
            .prefetch_related(
                Prefetch(
                    'comments',
                    queryset=Comment.objects.filter(approved=True)
                        .only('id', 'article', 'name', 'email', 'content', 'created_at')
                )
            ) \
            .order_by('-created_at')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(business_articles, 15)
        context['business_articles'] = paginator.get_page(page)
        context['current_category'] = slug
        return context
    
class DisplayResourceItems(HitCountMixin, TemplateView):
    template_name = "display-resources.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resources_list = ResourcesModel.objects.all().order_by('-created_at')

        page = self.request.GET.get('page', 1)
        paginator = Paginator(resources_list, 10)
        context['resource_list'] = paginator.get_page(page)

        return context
    
class ViewArticle(HitCountMixin, TemplateView):
    template_name = "view-article.html"

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(name="Wahid Business News")
        hit_count = HitCount.objects.get_for_object(website)
        HitCountMixin.hit_count(request, hit_count)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        article = get_object_or_404(
                Article.objects.only('id', 'slug', 'title', 'content', 'created_at')
                .prefetch_related(
                    Prefetch(
                        'comments',
                        queryset=Comment.objects.filter(approved=True)
                            .only('id', 'article', 'name', 'email', 'content', 'created_at')
                    )
                ),
                slug=slug
            )
        context['article'] = article
        return context
    
class SaveCommentView(View):
    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)

        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('comment')

        if not name or not email or not content:
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)
        
        comment = Comment.objects.create(
            article=article,
            name=name,
            email=email,
            content=content
        )

        rendered = render_to_string('partials/comment.html', {'comment': comment})
        response = HttpResponse(rendered)
        response['HX-Trigger'] = 'comment-added'
        
        return response