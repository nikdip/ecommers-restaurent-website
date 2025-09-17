from django.urls import path,include
from . import views
from paypal.standard.ipn import views as paypal_views  




# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('italian/',views.italian,name='italian'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:item_id>/<str:category>/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    
     # PayPal Buy Now
    path('buy-now/<int:item_id>/<str:category>/', views.buy_now, name='buy_now'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

]
    
    
  





# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)