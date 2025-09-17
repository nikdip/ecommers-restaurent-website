from django.db import models
from django.contrib.auth.models import User

class Indian_menu(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField()
    original_price = models.IntegerField()
    menu_image =models.ImageField(upload_to='menu_images')  # As we are using image field we have to intall 'pillow'. And we have to Define MEDIA_URL in settings.py file so that all folder should save in media directory

class Italian_menu(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField()
    original_price = models.IntegerField()
    menu_image =models.ImageField(upload_to='menu_images')


class Dessert_menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    original_price = models.IntegerField()
    menu_image = models.ImageField(upload_to='menu_images')

class Snacks_menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    original_price = models.IntegerField()
    menu_image = models.ImageField(upload_to='menu_images')

class Drinks_menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    original_price = models.IntegerField()
    menu_image = models.ImageField(upload_to='menu_images')    



    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username
    





class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image = models.ImageField(upload_to='cart_images/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=50, choices=[
        ('indian', 'Indian Cuisine'),
        ('italian', 'Italian Cuisine'),
        ('dessert', 'Desserts'),
        ('snack', 'Snacks'),
        ('drink', 'Drinks'),
    ])

    def __str__(self):
        return f"{self.item_name} - {self.quantity} pcs"

    def total_price(self):
        return self.item_price * self.quantity
