# Generated by Django 3.1.5 on 2021-03-05 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
    ]
