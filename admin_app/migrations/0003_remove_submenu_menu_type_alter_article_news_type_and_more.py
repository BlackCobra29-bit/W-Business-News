# Generated by Django 5.1.6 on 2025-04-05 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_mainmenu_resourcesmodel_subscriber_website_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submenu',
            name='menu_type',
        ),
        migrations.AlterField(
            model_name='article',
            name='news_type',
            field=models.CharField(choices=[('trucks_diesel', 'Trucks - Diesel Vehicle'), ('machineries_diesel', 'Machineries - Diesel Vehicle'), ('cars_diesel', 'Cars - Diesel Vehicle'), ('electric_vehicle', 'Electric Vehicle'), ('news_banks_financial', 'News - Banks & Financial'), ('regulations_banks_financial', 'Regulations - Banks & Financial'), ('news_logistics_transport', 'News - Logistics and Transport'), ('regulations_logistics_transport', 'Regulations - Logistics and Transport')], max_length=50, verbose_name='Article Category'),
        ),
        migrations.DeleteModel(
            name='MainMenu',
        ),
        migrations.DeleteModel(
            name='SubMenu',
        ),
    ]
