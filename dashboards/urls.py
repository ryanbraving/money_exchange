from django.urls import path

from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('my_sellings', views.dashboard, name='my_sellings'),
    path('my_buyings', views.dashboard, name='my_buyings'),

]
