# Generated by Django 2.2.5 on 2020-11-11 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201110_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/uploaded'),
        ),
    ]
