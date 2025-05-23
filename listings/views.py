from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Listing
from django.db.models import F, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from listings.choices import currencies_choices, how_much_choices, search_range_finder
from dashboards.models import Dashboard
from django.contrib.auth.decorators import login_required
from django.views.generic import View, CreateView, TemplateView, ListView, DetailView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from .forms import CreateListingForm
from django.http import HttpResponseRedirect, JsonResponse
from money_exchange.utils import STATUSES
import logging
logger = logging.getLogger(__name__)

CURRENCY_TO_COUNTRY = {
    "CAD": "ca",
    "USD": "us",
    "NZD": "nz",
    "EUR": "eu",
    "GBP": "gb",
    "IRR": "ir",
    "AUD": "au",
}


def index(request):
    listings = Listing.objects.order_by('-created').filter(is_published=True, status=STATUSES['ENABLED'])
    paginator = Paginator(listings, 10)  # Show 6 listings per page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    # listing = Listing.objects.filter(dashboard_set__isnull=False).exists()
    # print(listing)

    context = {
        'listings': paged_listings,

    }

    return render(request, 'listings/listings.html', context)


class DetailListing(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.object
        reverse_rate = listing.selling / listing.buying
        buyer_get = listing.buying
        net_selling = listing.selling - listing.service_fee_sell
        rate = listing.buying / net_selling
        selling_country_code = CURRENCY_TO_COUNTRY.get(listing.selling_currency, listing.selling_currency.lower())
        buying_country_code = CURRENCY_TO_COUNTRY.get(listing.buying_currency, listing.buying_currency.lower())

        status_display = listing.get_status_display() if hasattr(listing, 'get_status_display') else str(
            getattr(listing, 'status', ''))

        # Human-readable grabbed_by
        if hasattr(listing, 'grabbed_by') and hasattr(listing.grabbed_by, 'all'):
            grabbed_by_qs = listing.grabbed_by.all()
            if grabbed_by_qs.exists():
                grabbed_by_display = ", ".join(str(user) for user in grabbed_by_qs)
            else:
                grabbed_by_display = "not grabbed yet"
        else:
            grabbed_by_display = "not grabbed yet"

        context = {
            'listing': listing,
            'rate': rate,
            'buyer_get': buyer_get,
            'net_selling': net_selling,
            'reverse_rate': reverse_rate,
            'status_display': status_display,
            'grabbed_by_display': grabbed_by_display,
            'flag_selling': f"https://flagcdn.com/24x18/{selling_country_code}.png",
            'flag_buying': f"https://flagcdn.com/24x18/{buying_country_code}.png",
        }

        return context

#
# @login_required(login_url='login')
# def listing(request, pk):
#     listing = get_object_or_404(Listing, pk=pk)
#
#     reverse_rate = listing.selling / listing.buying
#     buyer_get = listing.buying
#     net_selling = listing.selling - listing.service_fee_sell
#     rate = listing.buying / net_selling
#     selling_country_code = CURRENCY_TO_COUNTRY.get(listing.selling_currency, listing.selling_currency.lower())
#     buying_country_code = CURRENCY_TO_COUNTRY.get(listing.buying_currency, listing.buying_currency.lower())
#
#     # Human-readable status for choices fields
#     status_display = listing.get_status_display() if hasattr(listing, 'get_status_display') else str(getattr(listing, 'status', ''))
#
#     # Human-readable grabbed_by
#     if hasattr(listing, 'grabbed_by') and hasattr(listing.grabbed_by, 'all'):
#         grabbed_by_qs = listing.grabbed_by.all()
#         if grabbed_by_qs.exists():
#             grabbed_by_display = ", ".join(str(user) for user in grabbed_by_qs)
#         else:
#             grabbed_by_display = "not grabbed yet"
#     else:
#         grabbed_by_display = "not grabbed yet"
#
#     context = {
#         'listing': listing,
#         'rate': rate,
#         'buyer_get': buyer_get,
#         'net_selling': net_selling,
#         'reverse_rate': reverse_rate,
#         'status_display': status_display,
#         'grabbed_by_display': grabbed_by_display,
#         'flag_selling': f"https://flagcdn.com/24x18/{selling_country_code}.png",
#         'flag_buying': f"https://flagcdn.com/24x18/{buying_country_code}.png",
#     }
#     return render(request, 'listings/listing_detail.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-created').filter(is_published=True, status=STATUSES['ENABLED'])

    selling_currency = ''
    buying_currency = ''

    # i_have
    if 'selling_currency' in request.GET:
        selling_currency = request.GET['selling_currency']
        if selling_currency:
            queryset_list = queryset_list.filter(selling_currency__exact=selling_currency)

    # i_want
    if 'buying_currency' in request.GET:
        buying_currency = request.GET['buying_currency']
        if buying_currency:
            queryset_list = queryset_list.filter(buying_currency__exact=buying_currency)

    if selling_currency and buying_currency and selling_currency == buying_currency:
        messages.error(request, 'Selling and buying currencies should be different')
        return redirect('search')

    # how_much
    if 'how_much' in request.GET:
        how_much = (request.GET['how_much'])
        if how_much:
            queryset_list = queryset_list.filter(
                i_have__lte=search_range_finder[how_much][1],
                i_have__gt=search_range_finder[how_much][0]
            )

    # --- Sorting Logic ---
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')

    if sort == 'exchange_rate':
        queryset_list = queryset_list.annotate(
            exchange_rate_annotated=ExpressionWrapper(
                F('buying') / F('selling'),
                output_field=FloatField()
            )
        )
        sort_field = 'exchange_rate_annotated'
    else:
        sort_field = sort

    if sort:
        if direction == 'desc':
            sort_field = '-' + sort_field
        queryset_list = queryset_list.order_by(sort_field)

    # --- Pagination ---
    paginator = Paginator(queryset_list, 10)
    page = request.GET.get('page')
    paged_queryset_list = paginator.get_page(page)

    context = {
        'listings': paged_queryset_list,
        'currencies_choices': currencies_choices,
        'how_much_choices': how_much_choices,
        'values': request.GET
    }
    return render(request, 'listings/listings.html', context)

def listings_table_partial(request):
    selling_currency = request.GET.get('selling_currency')
    buying_currency = request.GET.get('buying_currency')
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)

    # Only show published listings!
    listings = Listing.objects.filter(is_published=True)
    if selling_currency:
        listings = listings.filter(selling_currency=selling_currency)
    if buying_currency:
        listings = listings.filter(buying_currency=buying_currency)

    # Annotate exchange_rate for sorting
    listings = listings.annotate(
        exchange_rate_annotated=ExpressionWrapper(
            F('buying') * 1.0 / F('selling'),
            output_field=FloatField()
        )
    )

    # Sorting logic
    if sort:
        order_by = sort
        if order_by == 'exchange_rate':
            order_by = 'exchange_rate_annotated'
        if direction == 'desc':
            order_by = '-' + order_by
        listings = listings.order_by(order_by)

    # Pagination logic
    paginator = Paginator(listings, 20)  # 20 per page
    page_obj = paginator.get_page(page_number)
    context = {
        'listings': page_obj,
        'user': request.user,
    }
    html = render(request, 'listings/_listings_table_body.html', context).content.decode('utf-8')
    return JsonResponse({'html': html})

def range_slider(request):
    return render(request, 'listings/search_range_slider.html')

class UpdateListing(LoginRequiredMixin, UpdateView):
    fields = ('selling', 'buying', 'purpose', 'is_published', 'selling_currency', 'buying_currency')
    # fields = '__all__'
    model = Listing
    template_name_suffix = '_update_form'

    def get_queryset(self, *args, **kwargs):
        owner = self.request.user
        return self.model.objects.filter(user=owner, status=STATUSES['ENABLED'])

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateListing, self).get_context_data(*args, **kwargs)
        context['origin'] = self.kwargs.get('origin', '')
        return context


class DeleteListing(LoginRequiredMixin, generic.DeleteView):
    model = Listing
    # select_related = ("user", "group")
    success_url = reverse_lazy("listings")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id, status=STATUSES['ENABLED'])

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


# @login_required(login_url='login')
class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = CreateListingForm
    success_url = reverse_lazy("my_sellings")


    # def get_form_kwargs(self):
    #     # update super call if python < 3
    #     form_kwargs = super().get_form_kwargs()
    #     form_kwargs['user'] = self.request.user  # pass the 'user' in kwargs
    #     return form_kwargs

    def form_valid(self, form):

        listing = form.save(commit=False)
        listing.user = self.request.user  # use your own profile here
        listing.save()
        return redirect(reverse('my_sellings'))
        # return super().form_valid(form)
        # return HttpResponseRedirect(self.get_success_url())




