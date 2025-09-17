from django.urls import path,include
from . import views
from paypal.standard.ipn import views as paypal_views  
from .views import CustomPasswordChangeView




# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [


    path('', views.index, name='home'),
    path('contact/',views.contact,name='contact'),



    #======================= signup,login ,logout url =========================


    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout, name='logout'),





    #========================== profile page url ===================================


    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("change_password/", CustomPasswordChangeView.as_view(), name="change_password"),
    path('order_history/', views.order_history, name='order_history'),
    path('profile/order-status/', views.order_status, name='order_status'), 
    path('profile/order-details/<int:order_id>/', views.order_details, name='order_details'),  
  



    #=================================== cuisine url ===================================================

    path('indian/', views.indian, name='indian_menu'),
    path('italian/',views.italian,name='italian'),
    path('dessert/', views.dessert, name='dessert_menu'),
    path('snacks/', views.snacks, name='snacks_menu'),
    path('drinks/', views.drinks, name='drinks_menu'),



   #===================================== cart url ============================================


    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:item_id>/<str:category>/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    
    #==================================== PayPal Buy Now url ======================================
    path('buy-now/<int:item_id>/<str:category>/', views.buy_now, name='buy_now'),

    path('checkout-all/', views.checkout_all, name='checkout_all'),

    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

]
    
    
  





# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)