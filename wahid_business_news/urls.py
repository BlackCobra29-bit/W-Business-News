from django.contrib import admin
from django.urls import path, include
from App.views import UserIndex
from django.conf import settings
from froala_editor import views
from django.conf.urls.static import static
from admin_app.views import AdminAuthentication, AdminIndex, WriteArticle, ArticleManagement, UpdateArticle, DeleteArticleView, AccountSettings, PasswordAdminUpdateView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('froala_editor/',include('froala_editor.urls')),
    path('captcha/', include('captcha.urls')),
    # User URLs
    path("", UserIndex.as_view(), name="user-index-view"),
    # Admin URLs
    path("admin-auth/", AdminAuthentication.as_view(), name="admin-auth-view"),
    path("admin-dashboard/", AdminIndex.as_view(), name="admin-index-view"),
    path("write-article/", WriteArticle.as_view(), name="write-article-view"),
    path("article-management/", ArticleManagement.as_view(), name="article-management-view"),
    path("<slug:slug>/update-article/", UpdateArticle.as_view(), name="update-article-view"),
    path('<slug:slug>/delete-article/', DeleteArticleView.as_view(), name='delete-article-view'),
    path('account-settings/', AccountSettings.as_view(), name='account-settings-view'),
    path('update-password/', PasswordAdminUpdateView.as_view(), name='password-update-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)