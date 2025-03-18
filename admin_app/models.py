from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from froala_editor.fields import FroalaField

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = FroalaField(theme = 'dark')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if Article.objects.filter(slug=self.slug).exists():
                count = 1
                new_slug = f"{self.slug}-{count}"
                while Article.objects.filter(slug=new_slug).exists():
                    count += 1
                    new_slug = f"{self.slug}-{count}"
                self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']