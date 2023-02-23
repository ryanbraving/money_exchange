from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import datetime
# from dashboards.models import Dashboard
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



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
                  ('IRT', 'IRT')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, blank=True)
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, editable=False)

    selling = models.BigIntegerField(null=True)
    selling_currency = models.CharField(max_length=5, choices=sorted(CURRENCIES), default='CAD')
    buying = models.BigIntegerField(null=True)
    buying_currency = models.CharField(max_length=5, choices=sorted(CURRENCIES), default='IRT')
    purpose = models.CharField(max_length=20, choices=sorted(YEAR_IN_SCHOOL_CHOICES), default='TUITION_FEE')

    # price = models.DecimalField(max_digits=2, decimal_places=1)
    is_published = models.BooleanField(default=False)
    is_seller_deposited = models.BooleanField(default=False)
    is_buyer_deposited = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return '{} {} -> {} {}'.format(self.selling, self.selling_currency, self.buying, self.buying_currency)

    def seller_deposited(self):
        return 'Deposited' if self.is_seller_deposited else 'Not deposited'

    @property
    def service_fee(self):
        return int(self.buying * 0.005)

    @property
    def total(self):
        return int(self.buying + self.service_fee)

    def get_absolute_url(self):
        return reverse('detail_listing', kwargs={'pk': self.pk})
