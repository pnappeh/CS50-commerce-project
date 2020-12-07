from django.contrib import admin
from .models import User, Listing, Bid, Comment

class Listing_admin(admin.ModelAdmin):
    list_display = ("id", "name", "seller", "post_date")

class Bid_admin(admin.ModelAdmin):
    list_display = ("id", "bids", "potential_buyer", "product", "bid_date")

class Comment_admin(admin.ModelAdmin):
    list_display = ("id", "comment", "user_comment", "product")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, Listing_admin)
admin.site.register(Bid, Bid_admin)
admin.site.register(Comment, Comment_admin)