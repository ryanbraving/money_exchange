from django.db import models
# from datetime import datetime
from django.utils.timezone import datetime
from listings.models import Listing
from django.contrib.auth.models import User

class Dashboard(models.Model):
    ASK_TO_CHANGE_MESSAGES = [('only_have', 'I only have ...')]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    # listing = models.CharField(max_length=200)
    # listing_id = models.IntegerField()
    # listing_owner_name = models.CharField(max_length=100)
    # listing_owner_email = models.CharField(max_length=100)
    # requester_user_id = models.IntegerField()
    # requester_name = models.CharField(max_length=100)
    # requester_email = models.CharField(max_length=100)
    request_to_change = models.CharField(max_length=20, choices=sorted(ASK_TO_CHANGE_MESSAGES), default='TUITION_FEE', blank=True)
    message = models.TextField(blank=True)
    grabbing_date = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return f"{self.user}|{self.listing}"
