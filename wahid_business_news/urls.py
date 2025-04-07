from django.contrib import admin
from django.urls import path, include
from App.views import UserIndex, NewsByCategoryView, DisplayResourceItems, AboutUs
from django.conf import settings
from froala_editor import views
from App.views import NewsByCategoryView
from django.conf.urls.static import static
from admin_app.views import AdminAuthentication, AdminIndex, WriteArticle, ArticleManagement, UpdateArticle, DeleteArticleView, AddResources, DocumentManagement , UpdateResource, DeleteResourceView, SubscriberList, AccountSettings, PasswordAdminUpdateView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('captcha/', include('captcha.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    # User URLs
    path("", UserIndex.as_view(), name="user-index-view"),
    path('business_news/<slug:news_type>/', NewsByCategoryView.as_view(), name='news-by-category'),
    path("display-resources", DisplayResourceItems.as_view(), name = "display-resources"),
    path("about-us", AboutUs.as_view(), name = "about-us"),
    # Admin URLs
    path("admin-auth/", AdminAuthentication.as_view(), name="admin-auth-view"),
    path("admin-dashboard/", AdminIndex.as_view(), name="admin-index-view"),
    path("write-article/", WriteArticle.as_view(), name="write-article-view"),
    path("article-management/", ArticleManagement.as_view(), name="article-management-view"),
    path("<slug:slug>/update-article/", UpdateArticle.as_view(), name="update-article-view"),
    path('<slug:slug>/delete-article/', DeleteArticleView.as_view(), name='delete-article-view'),
    path('add-resources/', AddResources.as_view(), name = 'add-resources'),
    path("document-management/", DocumentManagement.as_view(), name="document-management-view"),
    path("<int:id>/update-resource/", UpdateResource.as_view(), name="update-resource-view"),
    path('<int:id>/delete-resource/', DeleteResourceView.as_view(), name='delete-resource-view'),
    path('blog-followers/', SubscriberList.as_view(), name = 'blog-followers'),
    path('account-settings/', AccountSettings.as_view(), name='account-settings-view'),
    path('update-password/', PasswordAdminUpdateView.as_view(), name='password-update-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)