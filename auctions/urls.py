from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("categories/<path:category>", views.categories_listings, name="categories_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("auctions<path:auction_url>", views.listing_view, name="listing_view"),
    path("add", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist_index, name="watchlist_index"),
    path("comment", views.comment, name="comment"),
    path("bid", views.bid, name="bid"),
    path("eliminate_listings", views.eliminate_listing, name="eliminate_listing"),
    path("older_posts", views.older_posts, name="older_posts")
] 