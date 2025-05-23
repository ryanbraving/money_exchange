from django.urls import path
from . import views

# app_name = 'listings'
urlpatterns = [
    path('', views.search, name='listings'),
    # path('detail_listing/<int:pk>', views.listing, name='detail_listing'),
    path('search', views.search, name='search'),
    # path('update/<int:pk>/', views.ListingUpdateView.as_view(), name="update"),
    path('update_listing/<int:pk>/<str:origin>', views.UpdateListing.as_view(), name='update_listing'),
    path('delete_listing/<int:pk>/', views.DeleteListing.as_view(), name='delete_listing'),
    path('create_listing/', views.CreateListing.as_view(), name='create_listing'),
    # path('redirect_listing/<int:pk>', views.RedirectListing.as_view(), name='redirect_listing'),
    path('range_slider', views.range_slider, name='range_slider'),
    path('<int:pk>/', views.DetailListing.as_view(), name="detail_listing"),
    path('table-partial/', views.listings_table_partial, name='listings_table_partial'),

]
