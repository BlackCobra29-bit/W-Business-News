# Generated by Django 5.1.6 on 2025-04-06 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_remove_submenu_menu_type_alter_article_news_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='full_content_url',
            field=models.URLField(blank=True, help_text='URL to the full content', null=True),
        ),
    ]
