'''
Contains urls for different app pages as well as the django admin site
'''

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    # Laundromat listings page
    path('listing/', views.laundromat_listing, name = 'laundromat_listing'),
    # Default home page
    path('home/', views.home_page, name = 'home_page'),    
    # Contact us page
    path('contact/', views.contact_us, name = 'contact_us'),
    # About page
    path('about/', views.about, name = 'about'),
]
