# Generated by Django 2.2.5 on 2020-11-20 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201116_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
