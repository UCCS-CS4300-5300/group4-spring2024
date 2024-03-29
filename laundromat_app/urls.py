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
    #delete a laundromat
    path('laundromats/<int:pk>/delete', views.LaundromatDeleteView.as_view(), name='laundromat_delete'),
    # View all machines in a laundromat 
    path('laundromats/<int:pk>/machines', views.MachineListView.as_view(), name ='machine_list'),
    #create a machine
    path('laundromats/<int:pk>/machines/create', views.MachineCreate.as_view(), name='machine_create'),
    #update a machine
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>/update', views.MachineUpdate.as_view(), name='machine_update'),
    #delete a machine
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>/delete', views.MachineDeleteView.as_view(), name='machine_delete'),
    #view the details of a single machine in a laundromat
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>', views.MachineDetailView.as_view(), name='machine_detail'),
    #new path to create the api listing, takes the request
    path('laundromat-listing/', views.laundromat_listing, name='laundromat_listing'),

]


