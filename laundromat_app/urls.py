'''
Contains urls for different app pages as well as the django admin site
'''

from django.contrib import admin
from django.urls import path
from . import views
from .views import CustomLogoutView, CustomLoginView, UnauthorizedView


urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    # Default home page
    path('', views.home_page, name = 'home_page'),
    #signup page
    path('signup', views.Signup.as_view(), name='signup'),
    #login page
    path('login/', CustomLoginView.as_view(), name='login'),
    #logoout page
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('unauthorized/', UnauthorizedView.as_view(), name='unauthorized_view'),
    # Machine list page
    #path('machines/', views.machine_list, name = 'machine_list'),
    # Reserve machine page
    path('reserve_machine/', views.reserve_machine, name='reserve_machine'),     
    # Contact us page
    path('contact/', views.contact_us, name = 'contact_us'),
    # About page
    path('about/', views.about, name = 'about'),
    # View all laundromats
    path('laundromats', views.LaundromatListView.as_view(), name ='laundromat_list'),
    #View the details of a single laundromat
    path('laundromats/<int:pk>', views.LaundromatDetailView.as_view(), name ='laundromat_detail'),
    # Create a laundromat
    path('laundromats/create', views.LaundromatCreate.as_view(), name ='laundromat_create'),
    # Update a laundromat
    path('laundromats/<int:pk>/update', views.LaundromatUpdate.as_view(),
         name ='laundromat_update'),
    #delete a laundromat
    path('laundromats/<int:pk>/delete', views.LaundromatDeleteView.as_view(),
         name='laundromat_delete'),
    #new path to create the api listing, takes the request
    path('laundromat-listing/', views.laundromat_listing, name='laundromat_listing'),
    # View all machines in a laundromat
    path('laundromats/<int:pk>/machines', views.MachineListView.as_view(), name ='machine_list'),
    #create a machine
    path('laundromats/<int:pk>/machines/create', views.MachineCreate.as_view(),
         name='machine_create'),
    #update a machine
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>/update',
         views.MachineUpdate.as_view(), name='machine_update'),
    #delete a machine
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>/delete',
         views.MachineDeleteView.as_view(), name='machine_delete'),
    #view the details of a single machine in a laundromat
    path('laundromats/<int:laundromat_pk>/machines/<int:pk>', views.MachineDetailView.as_view(),
         name='machine_detail'),
    path('laundromats/<str:place_id>/', views.LaundromatDetailView.as_view(),
         name='laundromat_detail'),
    #payment page
    path('payment/', views.ProcessPayment.as_view(), name = 'process_payment'),
    #page view upon a payment being submitted successfully
    path('success/', views.SuccessfulPayment.as_view(), name = 'successful_payment'),
    #customer cancels a payment
    path('cancel/', views.CancelPayment.as_view(), name = 'cancel_payment'),
]
