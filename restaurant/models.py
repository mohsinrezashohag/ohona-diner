from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

class Company(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    
class AboutUs(models.Model):
    title = models.CharField(max_length=255)  # Field for the title
    description = models.TextField()  # Field for the description
    image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)  # Field for the image

    def __str__(self):
        return self.title
    

class CompanyProfile(models.Model):
    # Basic company information
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='company_profile')
    description = models.TextField() 
    image = models.ImageField(upload_to='company_profile_images/', blank=True, null=True)
    
    # Contact details
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)

    # Social media links
    facebook_link = models.URLField(max_length=255, blank=True, null=True)
    instagram_link = models.URLField(max_length=255, blank=True, null=True)
    youtube_link = models.URLField(max_length=255, blank=True, null=True)
    twitter_link = models.URLField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)
    tiktok_link = models.URLField(max_length=255, blank=True, null=True)
    pinterest_link = models.URLField(max_length=255, blank=True, null=True)

    # Additional company details
    address = models.TextField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    services_offered = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Owner(models.Model):
    # Basic information
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='owners')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='owner_images/', blank=True, null=True)

    # Contact details
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Social media links
    facebook_link = models.URLField(max_length=255, blank=True, null=True)
    instagram_link = models.URLField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)
    twitter_link = models.URLField(max_length=255, blank=True, null=True)
    pinterest_link = models.URLField(max_length=255, blank=True, null=True)
    tiktok_link = models.URLField(max_length=255, blank=True, null=True)

    # Additional information
    role = models.CharField(max_length=100, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ContactUs(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"Contact for {self.company.name}"
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Required field
    status = models.BooleanField(default=True)  # Optional field with a default value
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  # Optional image field
    description = models.TextField(blank=True, null=True)  # Optional description field

    def __str__(self):
        return self.name
    
class Gallerycategory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Required field
    status = models.BooleanField(default=True)  # Optional field with a default value
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  # Optional image field
    description = models.TextField(blank=True, null=True)  # Optional description field

    def __str__(self):
        return self.name
    
class Gallery(models.Model):
    Gallerycategory = models.ForeignKey('Gallerycategory', on_delete=models.CASCADE, related_name='galleries')  
    image = models.ImageField(upload_to='gallery_images/', blank=False, null=False)
    status = models.BooleanField(default=True)  
    caption = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Gallery for {self.category.name} - {self.id}"
    

class MenuItem(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumb_image = models.ImageField(upload_to='menu_thumbs/', blank=True, null=True)
    hot_deal_status = models.BooleanField(default=False)
    vat_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) 
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.name
        
    # @property
    # def slug_name(self):
    #     return slugify(self.name)


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return f"Image for {self.menu_item.name}"
    


class Ingredient(models.Model):

    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='ingredients')  # Foreign key to MenuItem
    name = models.CharField(max_length=100)  
    quantity = models.CharField(max_length=50, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.name} for {self.menu_item.name}"
