# Generated by Django 5.1.6 on 2025-04-03 14:22

import admin_app.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0018_alter_article_news_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('resource_file', models.FileField(upload_to=admin_app.models.thumbnail_upload_to)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
                'ordering': ['-created_at'],
            },
        ),
    ]
