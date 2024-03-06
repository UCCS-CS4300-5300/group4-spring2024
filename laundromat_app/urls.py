'''
Contains urls for different app pages as well as the django admin site
'''

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    # Default home page
    path('', views.home_page, name = 'home_page'),    
    # Contact us page
    path('contact/', views.contact_us, name = 'contact_us'),
    # About page
    path('about/', views.about, name = 'about'),
    # View all laundromats 
    path('laundromats/', views.LaundromatListView.as_view(), name ='laundromat_list'),
    #View the details of a single laundromat
    path('laundromats/<int:pk>', views.LaundromatDetailView.as_view(), name ='laundromat_detail'),
    # Create a laundromat 
    path('laundromats/create', views.LaundromatCreate.as_view(), name ='laundromat_create'),
    # Update a laundromat 
    path('laundromats/<int:pk>/update', views.LaundromatUpdate.as_view(), name ='laundromat_update'),
]
