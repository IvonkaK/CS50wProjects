# Generated by Django 3.1.5 on 2021-03-05 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_category', to='auctions.category'),
        ),
    ]