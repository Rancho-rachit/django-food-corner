# Generated by Django 5.0.7 on 2024-10-17 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_dish_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.IntegerField(default=0)),
            ],
        ),
    ]