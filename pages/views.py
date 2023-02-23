from django.shortcuts import render
from listings.models import Listing
from listings.choices import currencies_choices, how_much_choices


def index(request):
    listings = Listing.objects.order_by('-created').filter(is_published=True)[:10]

    contex = {
        'listings': listings,
        'currencies_choices': currencies_choices,
        'how_much_choices': how_much_choices
    }
    return render(request, 'pages/index.html', contex)


def about(request):
    return render(request, 'pages/about.html')
