from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dashboard
# from django.contrib.auth.models import User
# from django.conf import settings
# from accounts.models import User
from django.contrib.auth import get_user_model
from listings.models import Listing


def dashboard(request):
    if request.method == 'POST':
        user_id = int(request.POST['user_id'])
        if not user_id:
            print("User is not logged in")
            messages.error(request, 'You need to login first')
            return redirect('login')

        user = get_object_or_404(get_user_model(), pk=user_id)

        listing_id = request.POST['listing_id']
        listing = get_object_or_404(Listing, pk=listing_id)

        if listing.user.id == user_id:
            messages.error(request, "This is your own listing. You can't grab it")
            return redirect('detail_listing', listing_id)


        # if user_id == listing.user.id:
        #     messages.error(request, 'This is your own listing')
        #     return redirect('detail_listing')

        # user_name = request.POST['user_name']
        # user_email = request.POST['user_email']
        # listing = request.POST['detail_listing']
        # listing_id = request.POST['listing_id']
        # listing_owner = request.POST['listing_owner']
        # listing_owner_email = request.POST['listing_owner_email']

        # if not Dashboard.objects.filter(listing=listing, requester_user_id=request.user.id).exists():
        if not Dashboard.objects.filter(listing=listing, user=user).exists():

            dashboard = Dashboard(listing=listing, user=user)
            dashboard.save()
            messages.success(request, 'You grabbed the deal.')
        else:
            messages.error(request, 'You have already grabbed this ...')

    my_buyings = []
    my_sellings = []
    # if 'my_buyings' in request.path:
    # my_buyings = Dashboard.objects.filter(user=request.user.id).order_by('-grabbing_date')
    # if 'my_sellings' in request.path:
    # my_sellings = Listing.objects.filter(user=request.user.id).order_by('-created')

    if 'my_buyings' in request.path:
        show_tab_selling = False
        my_buyings = Dashboard.objects.filter(user=request.user.id).order_by('-grabbing_date')
        # my_sellings = []
    elif 'my_sellings' in request.path:
        show_tab_selling = True
        my_sellings = Listing.objects.filter(user=request.user.id).order_by('-created')
        # my_buyings = []

    elif my_buyings and my_sellings:
        if my_sellings[0].updated > my_buyings[0].grabbing_date:
            show_tab_selling = True
        else:
            show_tab_selling = False
    elif my_buyings:
        show_tab_selling = False
    else:
        show_tab_selling = True


    contex = {'my_buyings': my_buyings,
              'my_sellings': my_sellings,
              'show_tab_selling': show_tab_selling}
    return render(request, 'dashboards/dashboard.html', contex)

def my_sellings(request):
    contex = {'my_sellings': my_sellings}
    return render(request, 'dashboards/dashboard.html', contex)

def my_buyings(request):
    contex = {'my_buyings': my_sellings}
    return render(request, 'dashboards/dashboard.html', contex)


