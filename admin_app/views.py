from .models import Article
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from .forms import Article_form
from django import forms
from captcha.fields import CaptchaField

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

class AdminAuthentication(TemplateView):
    template_name = "admin_templates/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate CAPTCHA
        captcha_form = CaptchaTestForm(request.POST)
        if not captcha_form.is_valid():
            return render(request, self.template_name, {"error": "Invalid CAPTCHA", "captcha_form": captcha_form})

        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Change to your dashboard URL
        else:
            return render(request, self.template_name, {"error": "Invalid credentials", "captcha_form": captcha_form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"captcha_form": CaptchaTestForm()})

class AdminIndex(TemplateView):
    template_name = "admin_templates/index.html"
    
class WriteArticle(TemplateView):
    template_name = "admin_templates/write_article.html"

    def post(self, request, *args, **kwargs):
        form = Article_form(request.POST, request.FILES)
        if form.is_valid():
            try:
                article = form.save()
                return JsonResponse({"success": True, "message": "Article published successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        else:
            return JsonResponse({"success": False, "message": "Invalid form data", "errors": form.errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Article_form()
        return context
    
class ArticleManagement(TemplateView):
    template_name = "admin_templates/article-management.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        articles = Article.objects.only('id', 'title', 'thumbnail', 'created_at', 'updated_at').all()

        context['articles'] = articles
        return context
    
class UpdateArticle(UpdateView):
    model = Article
    form_class = Article_form
    template_name = "admin_templates/update-article.html"
    success_url = reverse_lazy('article-management-view')

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=slug)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            try:
                article = form.save()
                return JsonResponse({"success": True, "message": "Article updated successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        else:
            return JsonResponse({"success": False, "message": "Invalid form data", "errors": form.errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context
    
class DeleteArticleView(View):
    def delete(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            article.delete()
            return JsonResponse({"success": True, "message": "Article deleted successfully!"})
        except Article.DoesNotExist:
            return JsonResponse({"success": False, "message": "Article not found!"})