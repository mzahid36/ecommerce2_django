from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','name','email','phone','gender','profile_pic']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','division','district','thana','holding_street_village','zipcode']

@admin.register(FoodItem)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['title','description','price','category','special','food_img']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','fooditem','quantity']

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','customer','add','fooditem','quantity','ordered_date','status']

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['name','designation','fb_link','tw_link','ins_link']

@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(GetInTouch)
class getintouchAdmin(admin.ModelAdmin):
    list_display = ['name','subject','email','message']

@admin.register(BookTable)
class BookTableAdmin(admin.ModelAdmin):
    list_display = ['name','email','persons','phone','date','note']

