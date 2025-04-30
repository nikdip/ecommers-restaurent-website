from django.contrib import admin
from .models import Indian_menu , Italian_menu, Drinks_menu ,Snacks_menu , Dessert_menu ,Profile,Cart, Order, OrderItem

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



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_name', 'item_price', 'quantity', 'category', 'total_price']
    list_filter = ['category', 'user']
    search_fields = ['item_name', 'user__username']
    readonly_fields = ['total_price']

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_date', 'status', 'total_price']
    list_filter = ['status', 'order_date']
    search_fields = ['user__username', 'id']
    date_hierarchy = 'order_date'
    ordering = ['-order_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'price', 'quantity', 'item_total']
    list_filter = ['order__status']
    search_fields = ['name', 'order__id']

    def item_total(self, obj):
        return obj.price * obj.quantity
    item_total.short_description = 'Item Total'




