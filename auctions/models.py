from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=255)
    starting_bid = models.PositiveIntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    details = models.TextField()
    post_date = models.DateTimeField()
    image = models.ImageField(upload_to="media/uploaded", blank=True, null=True)
    url = models.CharField(max_length=255, unique=True)
    categories = (
        ("1", "BOOKS"),
        ("2", "BUSINESS & INDUSTRIAL"),
        ("3", "CLOTHING, SHOES & ACCESSORIES"),
        ("4", "COLLECTIBLES"),
        ("5", "CONSUMER ELECTRONICS"),
        ("6", "CRAFTS"),
        ("7", "DOLLS & BEARS"),
        ("8", "HOME & GARDEN"),
        ("9", "MOTORS"),
        ("10", "PET SUPPLIES"),
        ("11", "SPORTING GOODS"),
        ("12", "SPORTS MEM, CARDS & FAN SHOP"),
        ("13", "TOYS & HOBBIES"),
        ("14", "ANTIQUES"),
        ("15", "COMPUTERS/TABLETS & NETWORKING"),
    )
    listing_category = models.CharField(max_length=150, choices=categories, default="1")
    states = (
        ("1", "ACTIVE"),
        ("2", "NOT ACTIVE")
    )
    state = models.CharField(max_length=64, choices=states, default="1")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="auction_winner")

    def __str__(self):
        return f"Listing {self.name} by {self.seller} posted on {self.post_date}"
class Bid(models.Model):
    bids = models.PositiveIntegerField()
    potential_buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="buyer")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    bid_date = models.DateTimeField()

class Comment(models.Model):
    comment = models.TextField(max_length=255)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_comment")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_comment")