from django.shortcuts import render,redirect,get_object_or_404
from .models import Indian_menu, Italian_menu,Dessert_menu,Snacks_menu,Drinks_menu,Profile ,Cart
from django.contrib.auth.models import User ,auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout 
from django.contrib import messages




from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse



# Create your views here.

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

    

def about(request):
    return render(request,'nikdip/about.html')

def contact(request):
    return render(request,'nikdip/contact.html')




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



@login_required
def logout(request):
    auth_logout(request)  
    messages.success(request, "You have successfully logged out.")
    return redirect('/')  

def italian(request):
    italian_menu = Italian_menu.objects.all()
    return render(request,'nikdip/italian.html',{"italian_menu": italian_menu,})



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



def increase_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')  # Redirects to the cart page

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # If quantity is 1 and user decreases, remove from cart
    return redirect('cart')



@login_required
def remove_from_cart(request, item_id):
    item = Cart.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('cart')




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

    # Generate a unique invoice ID
    invoice_id = str(uuid.uuid4())

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



def payment_success(request):
    messages.success(request, "Payment was successful! Your order is confirmed.")
    return render(request, 'nikdip/payment_success.html')

def payment_cancel(request):
    messages.error(request, "Payment was canceled. Please try again.")
    return render(request, 'nikdip/payment_cancel.html')

