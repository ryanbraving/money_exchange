from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Listing
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
from django.http import HttpResponseRedirect
from money_exchange.utils import STATUSES



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


@login_required(login_url='login')
def listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status=STATUSES['ENABLED'])

    # grabbed_by = Dashboard.objects.filter(listing=listing).order_by('grabbed_on').values_list('user__first_name',                                                                                flat=True)
    # grabbed_by = ' | '.join(list(grabbed_by))
    context = {
        'listing': listing,
        # 'grabbed_by': grabbed_by,
        'rate': listing.buying/listing.selling,
        'rate_reverse': listing.selling / listing.buying
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-created').filter(is_published=True, status=STATUSES['ENABLED'])

    selling_currency = ''
    buying_currency = ''

    # i_have
    if 'selling_currency' in request.GET:
        selling_currency = request.GET['selling_currency']
        if selling_currency:
            queryset_list = queryset_list.filter(buying_currency__exact=selling_currency)

    # i_want
    if 'buying_currency' in request.GET:
        buying_currency = request.GET['buying_currency']
        if buying_currency:
            queryset_list = queryset_list.filter(selling_currency__exact=buying_currency)

    if selling_currency and buying_currency and selling_currency==buying_currency:
        messages.error(request, 'Selling and buying currencies should be different')
        return redirect('search')

    # how_much
    if 'how_much' in request.GET:
        how_much = (request.GET['how_much'])
        print(search_range_finder[how_much][0])
        print(search_range_finder[how_much][1])
        if how_much:
            queryset_list = queryset_list.filter(i_have__lte=search_range_finder[how_much][1],
                                                 i_have__gt=search_range_finder[how_much][0])

    # dashboards = Dashboard.objects.filter(listing_id=)

    paginator = Paginator(queryset_list, 10)  # Show 6 listings per page
    page = request.GET.get('page')
    paged_queryset_list = paginator.get_page(page)

    context = {
        'listings': paged_queryset_list,
        'currencies_choices': currencies_choices,
        'how_much_choices': how_much_choices,
        'values': request.GET
    }
    return render(request, 'listings/listings.html', context)
    # return render(request, 'listings/search.html', context)


def range_slider(request):
    return render(request, 'listings/search_range_slider.html')

class UpdateListing(LoginRequiredMixin, UpdateView):
    fields = ('selling', 'buying', 'purpose', 'is_published')
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
class CreateListing(LoginRequiredMixin, generic.CreateView):
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




