# Generated by Django 5.1.6 on 2025-03-21 13:44

import admin_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0007_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='news_type',
            field=models.CharField(choices=[('diesel_vehicle', 'Diesel Vehicle'), ('electric_vehicle', 'Electric Vehicle'), ('banks_financial', 'Banks & Financial'), ('logistics_transport', 'Logistics and Transport')], default='diesel_vehicle', max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(upload_to=admin_app.models.thumbnail_upload_to),
        ),
    ]
