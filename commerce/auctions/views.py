from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Watchlist, Comment, Category, Bidding
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def index(request):
    # get active listings
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username and/or password.')
            return render(request, "auctions/login.html")

    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        if not username:
            messages.add_message(request, messages.ERROR, 'You must provide username')
            return render(request, "auctions/register.html")
        if not email:
            messages.add_message(request, messages.ERROR, 'You must provide email')
            return render(request, "auctions/register.html")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.add_message(request, messages.ERROR, 'Passwords must match.')
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'Username already taken.')
            return render(request, "auctions/register.html")

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required()
def create_listing(request):
    if request.method == "POST":

        # grab form data
        title = request.POST["title"]
        if not title:
            messages.add_message(request, messages.ERROR, 'Title cannot be empty')
            return render(request, "auctions/create_listing.html")

        desc = request.POST["desc"]
        if not desc:
            messages.add_message(request, messages.ERROR, 'Listing description cannot be empty')
            return render(request, "auctions/create_listing.html")

        start_price = request.POST["start_price"]
        if not start_price:
            messages.add_message(request, messages.ERROR, 'You must provide starting bid amount')
            return render(request, "auctions/create_listing.html")

        url = request.POST["url"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user

        # create new listing
        listing = Listing(
            title=title, description=desc, img_url=url, bidding_start=start_price, listing_category=category, user=user
        )
        listing.save()

        # set starting bidding amount as the current highest bid
        bidding = Bidding(listing=listing, user=user, amount_offered=start_price, is_user_listing_owner=True)
        bidding.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            'categories': categories
        })


def show_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    # listing comments to load
    comments = Comment.objects.filter(listing=listing)

    # get the current highest bid to display
    current_highest_bid = Bidding.objects.filter(listing=listing)
    value = current_highest_bid.order_by('-amount_offered').first()

    # get the total number of bids (-1 which is the first saved bid by the auction owner)
    total_bids = len(Bidding.objects.filter(listing=listing)) - 1

    # get and display the highest bidder if exists
    highest_bid = Bidding.objects.filter(listing=listing)
    highest = highest_bid.order_by('-amount_offered').first()
    if highest.is_auction_winner and not listing.is_active:
        auction_winner = highest.user
    else:
        auction_winner = "This auction is still active and there is no winner yet"

    return render(request, "auctions/show_listing.html", {
        "listing": listing,
        "comments": comments,
        "highest_bid": value.amount_offered,
        "current_winning_bidder": value.user.username,
        "total_bids": total_bids,
        "auction_winner": auction_winner
    })


def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        if not listing.is_active:
            messages.add_message(request, messages.ERROR, 'This auction is already closed')
            return redirect('showListing', listing_id=listing_id)
        listing.is_active = False
        listing.save()

        # find the highest bidder
        highest_bid = Bidding.objects.filter(listing=listing)
        highest = highest_bid.order_by('-amount_offered').first()
        # set the bidder to winner
        highest.is_auction_winner = True
        highest.save()

        messages.add_message(request, messages.SUCCESS, 'Auction has been closed successfully.')
        return redirect('showListing', listing_id=listing_id)


@login_required()
def watchlist(request):
    user = request.user
    # get user watchlist
    user_watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })


@login_required()
def add_to_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)

    # add new item to user's watchlist
    new_watchlist_item = Watchlist(user=user, listing=listing)
    new_watchlist_item.save()
    messages.add_message(request, messages.SUCCESS, 'Item was added to your watchlist')
    return redirect('showListing', listing_id=listing_id)


@login_required()
def remove_from_watchlist(request, watchlist_id):
    # Delete chosen element from user watchlist
    Watchlist.objects.filter(id=watchlist_id).delete()
    return redirect('watchlist')


@login_required()
def add_comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        content = request.POST['comment']
        if not content:
            messages.add_message(request, messages.ERROR, 'Comment field cannot be empty. Add comment.')
            return redirect('showListing', listing_id=listing_id)
        new_comment = Comment(user=user, listing=listing, content=content)
        new_comment.save()
        return redirect('showListing', listing_id=listing_id)


@login_required()
def categories(request):
    # get all categories
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })


@login_required()
def show_category_listings(request, category_id):
    # get all active listings based on category
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(listing_category=category, is_active=True)
    return render(request, "auctions/show_category_listings.html", {
        "category": category,
        "listings": listings
    })


@login_required()
def add_bidding(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)

        # validate bid input
        bid = request.POST["bid"]
        if not bid:
            messages.add_message(request, messages.ERROR, 'You must provide bid amount')
            return redirect('showListing', listing_id=listing_id)

        # check if the auction is not closed already
        if not listing.is_active:
            messages.add_message(request, messages.ERROR, 'This auction is closed')
            return redirect('showListing', listing_id=listing_id)

        # get the current highest value & check if bid amount offered is higher than current bid
        current_highest_bid = Bidding.objects.filter(listing=listing)
        value = current_highest_bid.order_by('-amount_offered').first()
        if int(bid) < value.amount_offered:
            messages.add_message(request, messages.ERROR, 'Your bid must be higher than the current highest bid')
            return redirect('showListing', listing_id=listing_id)

        # add bidding, don't have to specify that user is not bidding owner because it's done in model by default
        bidding = Bidding(listing=listing, user=user, amount_offered=bid)
        bidding.save()
        messages.add_message(request, messages.SUCCESS,
                             'Congrats! Your bid has been accepted. You are currently the highest bidder!')
        return redirect('showListing', listing_id=listing_id)
