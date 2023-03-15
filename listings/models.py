import uuid
from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings
# from accounts.models import User
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
# from dashboards.models import Dashboard
from django.urls import reverse
# from dashboards.models import Dashboard
from django.utils.translation import gettext_lazy as _

class ServiceFee(models.Model):
    created = models.DateTimeField(default=datetime.now)
    # modified = models.DateTimeField(auto_now=True, editable=False)
    selling_rate = models.DecimalField(max_digits=4, decimal_places=3, default=0.005)
    buying_rate = models.DecimalField(max_digits=4, decimal_places=3, default=0.005)

    def __str__(self):
        return "Seller rate: {} --- Buyer rate: {}".format(self.selling_rate, self.buying_rate)

class Listing(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ('TUITION_FEE', 'Tuition fee'),
        ('LOAN_REPAYMENT', 'Loan repayment'),
        ('HELP_MY_FAMILY', 'Help my family'),
        ('TRAVELING', 'Traveling'),
        ('GIFT', 'Gift'),
    ]
    CURRENCIES = [('NZD', 'NZD'),
                  ('USD', 'USD'),
                  ('MYR', 'MYR'),
                  ('CAD', 'CAD'),
                  ('IRR', 'IRR')]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, blank=True)
    # uuid = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, unique=True, editable=False)
    uuid = models.CharField(primary_key=False, max_length=8, db_index=True, default=uuid.uuid4, editable=False, unique=True)
    # id = models.BigAutoField(primary_key=False, db_index=True, editable=False, unique=True)

    selling = models.BigIntegerField(null=True)
    selling_currency = models.CharField(max_length=5, choices=sorted(CURRENCIES), default='CAD')
    buying = models.BigIntegerField(null=True)
    buying_currency = models.CharField(max_length=5, choices=sorted(CURRENCIES), default='IRR')
    purpose = models.CharField(max_length=20, choices=sorted(YEAR_IN_SCHOOL_CHOICES), default='TUITION_FEE')

    # price = models.DecimalField(max_digits=2, decimal_places=1)
    is_published = models.BooleanField(default=False)
    is_seller_deposited = models.BooleanField(default=False)
    is_buyer_deposited = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(default=datetime.now)

    service_rate = models.ForeignKey(ServiceFee, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {} -> {} {}'.format(self.selling, self.selling_currency, self.buying, self.buying_currency)

    def save(self, *args, **kwargs):
        self.uuid = str(self.uuid).split("-")[0]
        self.service_rate = ServiceFee.objects.last()
        super(Listing, self).save(*args, **kwargs)

    def seller_deposited(self):
        return 'Deposited' if self.is_seller_deposited else 'Not deposited'

    @property
    def service_fee_buy(self):
        return float(self.buying * self.service_rate.buying_rate)

    @property
    def service_fee_sell(self):
        return float(self.selling * self.service_rate.selling_rate)

    @property
    def buyer_to_pay(self):
        return float(self.buying + self.service_fee_buy)

    @property
    def seller_to_pay(self):
        return float(self.selling + self.service_fee_sell)

    @property
    def grabbed_by(self):
        return self.dashboard_set.values_list('user_id', flat=True)

    def get_absolute_url(self):
        return reverse('detail_listing', kwargs={'pk': self.pk})
