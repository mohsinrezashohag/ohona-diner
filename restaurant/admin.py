from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . models import *

# Register your models here.

admin.site.unregister(User)

# Register the User model with your custom UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add or override features here, e.g., custom fields, list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'email', 'phone')
    search_fields = ('company__name', 'email', 'phone')

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone')
    search_fields = ('name', 'company__name', 'email', 'phone')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('company', 'email', 'phone')
    search_fields = ('company__name', 'email', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)

@admin.register(Gallerycategory)
class GallerycategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('Gallerycategory', 'status', 'caption')
    search_fields = ('Gallerycategory__name', 'caption')
    list_filter = ('status',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'hot_deal_status', 'status')
    search_fields = ('name', 'category__name', 'company__name')
    list_filter = ('hot_deal_status', 'status')

@admin.register(MenuItemImage)
class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ('menu_item',)
    search_fields = ('menu_item__name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_item', 'quantity', 'created_at')
    search_fields = ('name', 'menu_item__name')
    list_filter = ('created_at', 'updated_at')