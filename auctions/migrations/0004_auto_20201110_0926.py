# Generated by Django 2.2.5 on 2020-11-10 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201110_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='price',
            new_name='starting_bid',
        ),
    ]
