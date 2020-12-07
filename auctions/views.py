from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
import datetime
from .models import User, Listing, Bid, Comment
import uuid
from django.db.models import Max

class NewEntrie(forms.Form):
    page_title = forms.CharField(label="Page Title", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    page_url = forms.CharField(label="Page URL", max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional URL for your product', 'class': 'form-control'}))
    category_choice = forms.ChoiceField(label="Page Category", choices=Listing.categories, widget=forms.Select(attrs={'class': 'custom-select', 'aria-label': 'Select a category for search'}))
    page_image = forms.FileField(label="Auction Image", required=False)
    product_description = forms.CharField(label="Product Description", widget=forms.Textarea(attrs={'placeholder': 'Insert a Product Description for other users', 'class': 'form-control', 'rows': '10'}))
    starting_bid = forms.IntegerField(label="Starting Bid", widget=forms.NumberInput(attrs={'placeholder': 'Bid in $USD', 'class': 'form-control'}))

class NewComment(forms.Form):
    comment = forms.CharField(label="Let others know your thoughts", max_length=1000, widget=forms.Textarea(attrs={'placeholder': 'Type here your comment', 'class': 'form-control', 'rows': '7'}))
    product_url = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

class Bid_form(forms.Form):
    bid = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '$USD', 'class': 'form-control col-lg-4 col-6 col-md-5'}))
    product_url = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

class Eliminate(forms.Form):
    product_url = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

def index(request):
    if "watchlist" not in request.session:
        request.session['watchlist'] = []
        set(request.session['watchlist'])
    watchlist_number = len(request.session['watchlist'])
    listings = Listing.objects.filter(state="1")
    maximo = []
    for i in listings:
        maximo.append(i.product.aggregate(max=Max('bids'))['max'])
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_number": watchlist_number,
        "index": True,
        "bids": maximo,
    })

def older_posts(request):
    if "watchlist" not in request.session:
        request.session['watchlist'] = []
        set(request.session['watchlist'])
    watchlist_number = len(request.session['watchlist'])
    listings = Listing.objects.filter(state="2")
    maximo = []
    for i in listings:
        maximo.append(i.product.aggregate(max=Max('bids'))['max'])
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_number": watchlist_number,
        "index": False,
        "bids": maximo,
        "old": True
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing._meta.get_field('listing_category').choices
    })

def categories_listings(request, category):
    watchlist_number = len(request.session['watchlist'])
    listings = Listing.objects.filter(listing_category=category, state = "1")
    maximo = []
    for i in listings:
        maximo.append(i.product.aggregate(max=Max('bids'))['max'])
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_number": watchlist_number,
        "categories": Listing._meta.get_field('listing_category').choices[int(category) - 1][1],
        "bids": maximo,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewEntrie(request.POST, request.FILES)
        if request.user.is_authenticated:
            if not form.is_valid():
                print("Invalid form")
                return HttpResponseRedirect(reverse("index"))
            else:
                name = form.cleaned_data['page_title']
                starting_bid = form.cleaned_data['starting_bid']
                details = form.cleaned_data['product_description']
                seller = request.user
                post_date = datetime.datetime.now()
                try:
                    image = form.cleaned_data['page_image']
                except:
                    print("No image")
                    image = None
                if request.POST['page_url'] != "":
                    url = f"/{request.user}/{form.cleaned_data['page_url'].lower()}"
                else:
                    url =f"/{request.user}/{uuid.uuid4()}"
                listing_category = str(form.cleaned_data['category_choice'])
                try:
                    new_auction = Listing(name=name, starting_bid=starting_bid, seller=seller, details=details, post_date=post_date, image=image, url=url, listing_category=listing_category)
                    new_auction.save()
                except:
                    return render(request, "auctions/apology.html", {
                        "message": "Missing some field or URL already taken"
                    })    
                print(f"Auction {name} saved successfully on {post_date}")
                return HttpResponseRedirect(reverse("index"))                   
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": Listing.categories,
            "form": NewEntrie()
        })

def listing_view(request, auction_url):
    if auction_url in request.session['watchlist']:
        watchlist_item = True
    else:
        watchlist_item = False
    product = Listing.objects.get(url=auction_url)
    max_bid = Bid.objects.filter(product=product).aggregate(max=Max('bids'))
    if max_bid:
        min_value = max_bid['max']
    else:
        min_value = product.starting_bid
    return render(request, "auctions/auctions_entries.html", {
        "listings": product,
        "watchlist_item": watchlist_item,
        "auction_url": auction_url,
        "comment": NewComment(initial={'product_url': auction_url}),
        "auction_comments": Comment.objects.filter(product=product),
        "bid_form": Bid_form(initial={'product_url': auction_url}),
        "bids": Bid.objects.filter(product=product),
        'max_bid': max_bid['max'],
        "eliminate": Eliminate(initial={'product_url': auction_url}),
        "winner": product.winner
    })

@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        new_item = request.POST['watchlist']
        request.session['watchlist'] += [new_item]
        print(f"Item {new_item} added to {request.user.username} watchlist")
        return HttpResponseRedirect(reverse('listing_view', kwargs={'auction_url': new_item}))

@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        remove_item = request.POST['remove_from_watchlist']
        request.session['watchlist'].remove(remove_item)
        request.session.modified = True
        print(f"Item {remove_item} removed from {request.user.username} watchlist")
        print(request.session['watchlist'])
        return HttpResponseRedirect(reverse('listing_view', kwargs={'auction_url': remove_item}))

@login_required
def watchlist_index(request):
    watchlist_number = len(request.session['watchlist'])
    listings = Listing.objects.filter(url__in=(request.session['watchlist']))
    maximo = []
    for i in listings:
        maximo.append(i.product.aggregate(max=Max('bids'))['max'])
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_number": watchlist_number,
        "index": False,
        "bids": maximo
    })

@login_required
def comment(request):
    if request.method == "POST":
        form = NewComment(request.POST)
        if not form.is_valid():
            print("Invalid form")
            return HttpResponseRedirect(reverse("index"))
        else:
            user = request.user
            url = form.cleaned_data['product_url']
            product = Listing.objects.get(url=url)
            comment = form.cleaned_data['comment']
            new_comment = Comment(comment = comment, user_comment = user, product = product)
            new_comment.save()
            print(f"Comment from {user} in auction {product} saved")
            return HttpResponseRedirect(reverse('listing_view', kwargs={'auction_url': url}))

@login_required
def bid(request):
    if request.method == "POST":
        form = Bid_form(request.POST)
        if not form.is_valid():
            print("Invalid Bid, possible CSRF attack")
            return HttpResponseRedirect(reverse("index"))
        else:
            buyer = request.user
            url = form.cleaned_data['product_url']
            product = Listing.objects.get(url=url)
            bid_price = form.cleaned_data['bid']
            max_bid = Bid.objects.filter(product=product).aggregate(max=Max('bids'))
            if max_bid['max']:
                if bid_price > int(max_bid['max']):
                    new_bid = Bid(bids=bid_price, potential_buyer= buyer, product=product, bid_date= datetime.datetime.now())
                    new_bid.save()
                else:
                    return render(request, "auctions/apology.html", {
                        "message": "Bid must be higher than actual bid"
                    })
            else:
                if bid_price >= product.starting_bid:
                    new_bid = Bid(bids=bid_price, potential_buyer= buyer, product=product, bid_date= datetime.datetime.now())
                    new_bid.save()
                else:
                    return render(request, "auctions/apology.html", {
                        "message": "Bid must be equal or higher than starting bid"
                    })
            return HttpResponseRedirect(reverse('listing_view', kwargs={'auction_url': url}))

def eliminate_listing(request):
    if request.method == "POST":
        form = Eliminate(request.POST)
        if not form.is_valid():
            print("Invalid Auction Deactivation, possible CSRF attack")
            return HttpResponseRedirect(reverse("index"))
        else:
            url = form.cleaned_data['product_url']
            deactivated_product = Listing.objects.get(url = url)
            winner_price = deactivated_product.product.aggregate(max=Max('bids'))['max']
            winner_bid = Bid.objects.get(bids=winner_price, product=deactivated_product)
            winner = winner_bid.potential_buyer
            deactivated_product.winner = winner
            deactivated_product.state = "2"
            deactivated_product.save()
        return HttpResponseRedirect(reverse('index'))
            