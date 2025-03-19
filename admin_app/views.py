from .models import Article
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from .forms import Article_form
from django import forms
from captcha.fields import CaptchaField

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()
    
class AuthRequiredMixin(LoginRequiredMixin):
    login_url = "/admin-auth/?next=not-authenticated"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

class AdminAuthentication(TemplateView):
    template_name = "admin_templates/login.html"

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            
            return redirect("write-article-view")
            
        captcha_key = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_key)

        return self.render_to_response({
            "captcha_image": captcha_image,
            "captcha_key": captcha_key
        })

    def post(self, request, *args, **kwargs):
        username = request.POST.get("login_username")
        password = request.POST.get("login_password")
        captcha_key = request.POST.get("captcha_0")
        captcha_value = request.POST.get("captcha_1")

        try:
            captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha_obj.response.lower() != captcha_value.lower():
                messages.error(request, "Invalid CAPTCHA.")
                return self.redirect_with_query_params(request, "invalid-captcha")
        except CaptchaStore.DoesNotExist:
            messages.error(request, "Invalid CAPTCHA.")
            return self.redirect_with_query_params(request, "invalid-captcha")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("write-article-view")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name)

    def redirect_with_query_params(self, request, error_type):
        return redirect(f"{reverse('admin-auth-view')}?error={error_type}")

class AdminIndex(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/index.html"
    
class WriteArticle(AuthRequiredMixin, TemplateView):
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
    
class ArticleManagement(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/article-management.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        articles = Article.objects.only('id', 'title', 'thumbnail', 'created_at', 'updated_at').all()

        context['articles'] = articles
        return context
    
class UpdateArticle(AuthRequiredMixin, UpdateView):
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
    
class DeleteArticleView(AuthRequiredMixin, View):
    def delete(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            article.delete()
            return JsonResponse({"success": True, "message": "Article deleted successfully!"})
        except Article.DoesNotExist:
            return JsonResponse({"success": False, "message": "Article not found!"})