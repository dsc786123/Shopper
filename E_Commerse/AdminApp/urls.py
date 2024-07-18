from django.urls import path
from . import views
urlpatterns = [
path('home/',views.home),
path('addproduct/',views.addproduct),
path('addproductimage/',views.addproductimage),
path('changepassword/',views.changepassword),
path('editprofile/',views.editprofile),
path('managecustomer/',views.managecustomer),
path('managecustomerstatus/',views.managecustomerstatus),
path('managecustomer/delete/',views.deletecustomer)
]