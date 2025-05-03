from .models import Article, ResourcesModel, Subscriber
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.views import View
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.models import User
from .forms import Article_form , ResourcesForm, UserModelForm, CustomPasswordChangeForm
from django import forms
from captcha.fields import CaptchaField
from hitcount.models import HitCount

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
            return redirect("admin-index-view")
        
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
                return JsonResponse({"error": "Invalid CAPTCHA."}, status=400)
        except CaptchaStore.DoesNotExist:
            return JsonResponse({"error": "Invalid CAPTCHA."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"redirect": reverse("admin-index-view")})
        else:
            return JsonResponse({"error": "Invalid username or password."}, status=400)

class AdminIndex(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_count'] = Article.objects.aggregate(count=Count('id'))['count']
        total_hits = HitCount.objects.aggregate(total=Sum('hits'))['total'] or 0
        context['total_pageviews'] = total_hits
        total_subscribers = Subscriber.objects.count()
        context['total_subscribers'] = total_subscribers
        total_resources = ResourcesModel.objects.count()
        context['total_resources'] = total_resources
        return context
    
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
        
class AddResources(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/add_resources.html"

    def post(self, request, *args, **kwargs):
        form = ResourcesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                article = form.save()
                return JsonResponse({"success": True, "message": "Resource item added successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        else:
            return JsonResponse({"success": False, "message": "Invalid form data", "errors": form.errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResourcesForm()
        return context
    
class DocumentManagement(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/resources-management.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        resources = ResourcesModel.objects.only('id', 'resource_name', 'short_description', 'created_at').all()

        context['resources'] = resources
        return context
    
class UpdateResource(AuthRequiredMixin, UpdateView):
    model = ResourcesModel
    form_class = ResourcesForm
    template_name = "admin_templates/update-resource.html"
    success_url = reverse_lazy('document-management-view')

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(ResourcesModel, id=id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            try:
                resource = form.save()
                return JsonResponse({"success": True, "message": "Resource updated successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        else:
            return JsonResponse({"success": False, "message": "Invalid form data", "errors": form.errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context
    
class DeleteResourceView(AuthRequiredMixin, View):
    def delete(self, request, id):
        try:
            article = ResourcesModel.objects.get(id=id)
            article.delete()
            return JsonResponse({"success": True, "message": "Resource deleted successfully!"})
        except ResourcesModel.DoesNotExist:
            return JsonResponse({"success": False, "message": "Resource not found!"})
        
class SubscriberList(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/subscriber-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribers'] = Subscriber.objects.all()
        return context
        
class AccountSettings(AuthRequiredMixin, TemplateView):
    template_name = "admin_templates/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["form"] = UserModelForm(instance=self.request.user)
        context["password_form"] = CustomPasswordChangeForm(user=self.request.user)  # ðŸ‘ˆ Pass the password form
        return context

    def post(self, request, *args, **kwargs):
        form = UserModelForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Account information updated successfully!"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "message": "There was an error updating the account details.", "errors": errors})

class PasswordAdminUpdateView(AuthRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'admin_templates/update-password.html'
    success_url = reverse_lazy('admin-index-view')

    def form_valid(self, form):
        messages.success(self.request, 'Password updated successfully!')
        return super().form_valid(form)

class LogoutView(AuthRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(f"{reverse('admin-auth-view')}?logged_out_successfully=true")