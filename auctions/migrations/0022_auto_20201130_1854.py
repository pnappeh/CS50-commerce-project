# Generated by Django 2.2.5 on 2020-11-30 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20201129_1644'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]
