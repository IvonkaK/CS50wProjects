from django.contrib import admin

from .models import User, Listing, Watchlist, Comment, Category, Bidding

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Bidding)
