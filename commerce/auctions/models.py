from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    bidding_start = models.DecimalField(max_digits=19, decimal_places=2)
    img_url = models.URLField(blank=True, null=True)
    listing_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listing_category", blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    is_active = models.BooleanField(default=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    content = models.CharField(max_length=500)


class Bidding(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidding_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    amount_offered = models.DecimalField(max_digits=19, decimal_places=2)
    is_user_listing_owner = models.BooleanField(default=False)
    is_auction_winner = models.BooleanField(default=False)
