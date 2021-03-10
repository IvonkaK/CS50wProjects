from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createListing"),
    path("showListing/<int:listing_id>", views.show_listing, name="showListing"),
    path("closeListing/<int:listing_id>", views.close_listing, name="closeListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addToWatchlist/<int:listing_id>", views.add_to_watchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:watchlist_id>", views.remove_from_watchlist, name="removeFromWatchlist"),
    path("addComment/<int:listing_id>", views.add_comment, name="addComment"),
    path("categories", views.categories, name="categories"),
    path("showCategoryListings/<int:category_id>", views.show_category_listings, name="showCategoryListings"),
    path("addBidding/<int:listing_id>", views.add_bidding, name="addBidding")
]
