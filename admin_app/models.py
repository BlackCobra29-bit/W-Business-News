from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
from froala_editor.fields import FroalaField

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
    NEWS_TYPES = [
        ('Diesel Vehicle', 'Diesel Vehicle'),
        ('Electric Vehicle', 'Electric Vehicle'),
        ('Banks & Financial', 'Banks & Financial'),
        ('Logistics and Transport', 'Logistics and Transport'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = FroalaField(theme='dark')
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to)
    news_type = models.CharField(max_length=50, choices=NEWS_TYPES, default='diesel_vehicle')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

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