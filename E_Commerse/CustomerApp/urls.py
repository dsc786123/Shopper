from django.urls import path
from . import views
urlpatterns = [
path('home/',views.home),
path('cart/',views.cart),
path('cart/delete/',views.deleteproduct),
path('productdetails/',views.productdetails),
path('customerdetails/',views.customerdetails),
path('payment/',views.payment),
path('changepassword/',views.changepassword),
path('editprofile/',views.editprofile),
path('order/',views.order),
path('wishlist/',views.wishlist),
path('paymenthandler/', views.paymenthandler),
path('paymentstatus/',views.paymentstatus),
path('msg/',views.msg),
path('logout/',views.Logout),
]