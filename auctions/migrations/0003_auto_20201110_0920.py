# Generated by Django 2.2.5 on 2020-11-10 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listings_bids_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('details', models.TextField()),
                ('post_date', models.DateTimeField()),
                ('image', models.ImageField(blank=True, height_field=150, null=True, upload_to='', width_field=150)),
                ('url', models.URLField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='bids',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='auctions.Listings'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_comment', to='auctions.Listings'),
        ),
        migrations.DeleteModel(
            name='Auction_Listings',
        ),
    ]
