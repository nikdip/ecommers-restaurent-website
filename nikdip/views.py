from django.shortcuts import render,redirect,get_object_or_404
from .models import Indian_menu, Italian_menu,Dessert_menu,Snacks_menu,Drinks_menu,Profile ,Cart,Order,OrderItem
from django.contrib.auth.models import User ,auth

#======================================== login ,signup ,logout ,profile ,change pass library ===========================================

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout 
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



#================buy now or paypal library ===============================

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.db import transaction


import time




#========================== Create your views here.============================================

def index(request):
    indian_cuisine = Indian_menu.objects.all()
    italian_menu = Italian_menu.objects.all()
    desserts = Dessert_menu.objects.all()
    snacks = Snacks_menu.objects.all()
    drinks = Drinks_menu.objects.all()

    return render(request, 'nikdip/index.html', {
        "indian_cuisine": indian_cuisine,
        "italian_menu": italian_menu,
        "desserts": desserts,
        "snacks": snacks,
        "drinks": drinks
    })


def contact(request):
    return render(request,'nikdip/contact.html')




#================================== signup , login ,logout,profile function =====================================================



#signup function

def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken! Try another.")
            return redirect('signup')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists!")
            return redirect('signup')

       
        user = User.objects.create_user(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            username=username, 
            password=password1
        )
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return render(request, 'nikdip/login.html') 

    return render(request, 'nikdip/sign-up.html')



#login function

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  

        if user is not None:
            auth_login(request, user)  
            messages.success(request, "Login successful!")
            return redirect('/')  
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  

    return render(request, 'nikdip/login.html')




#profile function

@login_required
def profile(request):
    return render(request, 'nikdip/profile.html', {'user': request.user})

def edit_profile(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        profile.phone = phone
        profile.address = address

        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'nikdip/edit_profile.html', {'user': request.user})



#password change function

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "nikdip/change_password.html"  
    success_url = reverse_lazy("profile")  


#profile view function    

@login_required
def profile_view(request):
    return render(request, "nikdip/profile.html")  



#logout function

@login_required
def logout(request):
    auth_logout(request)  
    messages.success(request, "You have successfully logged out.")
    return redirect('/') 







#======================================= different cuisine function==========================================


def indian(request):
    indian_menu = Indian_menu.objects.all()
    return render(request, 'nikdip/menucard.html', {"indian_menu": indian_menu})



def italian(request):
    italian_menu = Italian_menu.objects.all()
    return render(request,'nikdip/italian.html',{"italian_menu": italian_menu,})


def dessert(request):
    dessert_menu = Dessert_menu.objects.all()
    return render(request, 'nikdip/dessert.html', {"dessert_menu": dessert_menu})

# View for Snacks Cuisine Menu
def snacks(request):
    snacks_menu = Snacks_menu.objects.all()
    return render(request, 'nikdip/snacks.html', {"snacks_menu": snacks_menu})

# View for Drinks Cuisine Menu
def drinks(request):
    drinks_menu = Drinks_menu.objects.all()
    return render(request, 'nikdip/drinks.html', {"drinks_menu": drinks_menu})






#========================================= add to cart function=============================================

@login_required
def add_to_cart(request, item_id, category):
    model_map = {
        "indian": Indian_menu,
        "italian": Italian_menu,
        "dessert": Dessert_menu,
        "snack": Snacks_menu,
        "drink": Drinks_menu,
    }

    if category not in model_map:
        return redirect('cart')

    item_model = model_map[category]
    item = item_model.objects.get(id=item_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item_name=item.name,
        item_price=item.original_price,
        item_image=item.menu_image,
        category=category,
        defaults={"quantity": 1},
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.item_price * item.quantity for item in cart_items)
    
    return render(request, 'nikdip/cart.html', {
        "cart_items": cart_items,
        "total_price": total_price
    })




# incresase quantity function

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')  



# decresase quantity function

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  
    return redirect('cart')



# remove product function

@login_required
def remove_from_cart(request, item_id):
    item = Cart.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


#========================================= order status and history ===============================================



#order history function

@login_required
def order_history(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-order_date')  
    
    
    return render(request, 'nikdip/order_history.html', {'orders': orders})




#order status function

@login_required
def order_status(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    return render(request, 'nikdip/order_status.html', {'orders': orders})




# order details function

@login_required
def order_details(request, order_id):
    
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'nikdip/order_details.html', {'order': order})





#=========================================== buy now function ========================================================


@login_required
def buy_now(request, item_id, category):
    # Map categories to models
    model_map = {
        'indian': Indian_menu,
        'italian': Italian_menu,
        'dessert': Dessert_menu,
        'snacks': Snacks_menu,
        'drinks': Drinks_menu,
    }

    # Get the correct model and fetch the item
    model = model_map.get(category)
    if not model:
        return render(request, 'nikdip/error.html', {'message': 'Invalid category'})

    item = get_object_or_404(model, id=item_id)


    invoice_id = str(uuid.uuid4())

    
    with transaction.atomic():
        # Create a new Order
        order = Order.objects.create(
            user=request.user,
            total_price=item.original_price,  
            status='Pending',  
        )

        
        OrderItem.objects.create(
            order=order,
            name=item.name,
            price=item.original_price,
            quantity=1  # 
        )

        # PayPal form data
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": item.original_price,
            "item_name": item.name,
            "invoice": invoice_id,
            "currency_code": "USD",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('payment_success')),
            "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'nikdip/buy_now.html', {
        'item': item,
        'form': form,
        'category': category
    })


# payment success function

def payment_success(request):
    # Find the most recent order (assuming a single item purchase in this case)
    order = Order.objects.filter(user=request.user).latest('order_date')
    order.status = 'Completed'
    order.save()

    messages.success(request, "Payment was successful! Your order is confirmed.")
    return render(request, 'nikdip/payment_success.html')



#payment cancle function

def payment_cancel(request):
    messages.error(request, "Payment was canceled. Please try again.")
    return render(request, 'nikdip/payment_cancel.html')




@login_required
def checkout_all(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')
    
    # Calculate total amount
    total = sum(item.item_price * item.quantity for item in cart_items)
    
    # Create a PayPal payment for the total amount
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": "Complete Order from NikDip",
        "invoice": f"INV-{request.user.id}-{int(time.time())}",
        "currency_code": "INR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
    }
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'nikdip/checkout-all.html', {'form': form, 'total': total})

