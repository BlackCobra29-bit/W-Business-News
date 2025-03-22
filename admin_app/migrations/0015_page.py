# Generated by Django 5.1.6 on 2025-03-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0014_delete_pageviewcounter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
