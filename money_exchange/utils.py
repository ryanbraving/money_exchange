from django.conf import settings

STATUS_CHOICES = getattr(settings, 'STATUS_CHOICES', (
    (0, 'Enabled'),
    (1, 'Suspended'),
    (2, 'Disabled'),
))

STATUSES = dict((v.upper(), k) for (k, v) in STATUS_CHOICES)
