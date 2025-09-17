from django.contrib import admin
from .models import Indian_menu , Italian_menu, Drinks_menu ,Snacks_menu , Dessert_menu ,Profile

@admin.register(Indian_menu)
class Indian_menuAdmin(admin.ModelAdmin):
    list_display= ['name','description','original_price','menu_image']


@admin.register(Italian_menu)
class Italian_menuAdmin(admin.ModelAdmin):
    list_display= ['name','description','original_price','menu_image']


@admin.register( Dessert_menu)
class  Dessert_menuAdmin(admin.ModelAdmin):
    list_display= ['name','description','original_price','menu_image']


@admin.register(Snacks_menu)
class Snacks_menuAdmin(admin.ModelAdmin):
    list_display= ['name','description','original_price','menu_image']


@admin.register(Drinks_menu)
class Drinks_menuAdmin(admin.ModelAdmin):
    list_display= ['name','description','original_price','menu_image']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display= ['user','phone','address','image']





