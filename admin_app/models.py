from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

NEWS_TYPE_CHOICES = (
    ('trucks_diesel', 'Trucks - Diesel Vehicle'),
    ('machineries_diesel', 'Machineries - Diesel Vehicle'),
    ('cars_diesel', 'Cars - Diesel Vehicle'),
    ('electric_vehicle', 'Electric Vehicle'),
    ('news_banks_financial', 'News - Banks & Financial'),
    ('regulations_banks_financial', 'Regulations - Banks & Financial'),
    ('news_logistics_transport', 'News - Logistics and Transport'),
    ('regulations_logistics_transport', 'Regulations - Logistics and Transport'),
)

class Website(models.Model):
    name = models.CharField(max_length=100, default="Wahid Business News")

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

def thumbnail_upload_to(instance, filename):
    return f'thumbnails/{filename[:100]}'

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to)
    news_type = models.CharField(
        max_length=50,
        choices=NEWS_TYPE_CHOICES,
        verbose_name="Article Category"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    full_content_url = models.URLField(blank=True, null=True, help_text="URL to the full content")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

        if self.thumbnail:
            img = Image.open(self.thumbnail.path)
            img = img.resize((1024, 576), Image.LANCZOS)
            img.save(self.thumbnail.path)

    def __str__(self):
        return self.title
    
class ResourcesModel(models.Model):
    resource_name = models.CharField(max_length=200)
    short_description = models.TextField()
    resource_file = models.FileField(upload_to="resources")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ['-created_at']

    def __str__(self):
        return self.resource_name