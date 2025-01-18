from django.urls import path
from . import views
from . import views_admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    # path('menu-ohana/', views.menu_ohana, name='menu_ohana'),
    # path('menu-sunny-side-up/', views.menu_sunny_side_up, name='menu_sunny_side_up'),
    # path('menu-mini-malaysia/', views.menu_mini_malaysia, name='menu_mini_malaysia'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('send-whatsapp/', views.send_whatsapp_message, name='send_whatsapp_message'),

# frontend menu company
    path('menu/<str:company_slug>/<int:company_id>/', views.menu_items, name='nav_menu'),
    path('menu/<str:menu_slug>/<int:company_id>/<int:menu_id>/', views.menu_single, name='menu_single'),

    # Admin Urls
    path('user/home/', views_admin.home_admin, name='home_admin'),

    path('user/login/', views_admin.login_admin, name='login_admin'),
    
    path('user/logout/', views_admin.logout_view, name='logout'),

    # About Us
    path('user/about-us-create/', views_admin.about_us_create, name='about_us_create'),
    path('user/about-us-list/', views_admin.about_us_list, name='about_us_list'),
    path('user/about-us-update/', views_admin.about_us_update, name='about_us_update'),
    path('user/delete-about-us/', views_admin.delete_about_us, name='delete_about_us'),

    # Company Profile
    path('user/company-profile-list/', views_admin.company_profile_list, name='company_profile_list'),
    path('user/company-profile-create/', views_admin.company_profile_create, name='company_profile_create'),
    path('user/company-profile-delete/', views_admin.company_profile_delete, name='company_profile_delete'),
    
    # Owner Profile
    path('user/owner-profile-create/', views_admin.owner_profile_create, name='owner_profile_create'),
    path('user/owner-profile-list/', views_admin.owner_profile_list, name='owner_profile_list'),
    path('user/owowner-profile-delete/', views_admin.owner_profile_delete, name='owner_profile_delete'),

    
    path('user/add_contactus_admin/', views_admin.add_contactus_admin, name='add_contactus_admin'),
    path('user/contactus_admin/', views_admin.contactus_admin, name='contactus_admin'),
    path('user/edit_contactus_admin/<int:contact_id>/', views_admin.edit_contactus_admin, name='edit_contactus_admin'),
    path('user/delete_contactus_admin/<int:contact_id>/', views_admin.delete_contactus_admin, name='delete_contactus_admin'),

    path('user/company/add/', views_admin.add_company, name='add_company'),
    path('user/edit_company/<int:company_id>', views_admin.edit_company, name='edit_company'),


    path('user/company/delete/<int:company_id>/', views_admin.delete_company, name='delete_company'), 
    path('user/company/list/', views_admin.company_list, name='company_list'), 

    path('user/add-category/', views_admin.add_category, name='add_category'),
    path('user/edit-category/<int:category_id>/', views_admin.edit_category, name='edit_category'),
    path('user/delete-category/<int:category_id>/', views_admin.delete_category, name='delete_category'),
        path('user/list-categories/', views_admin.list_categories, name='list_categories'),

    path('user/gallery/list/', views_admin.list_galleries, name='list_galleries'),
    path('user/gallery/add/', views_admin.add_gallery, name='add_gallery'),
 
    path('user/gallery/edit/<int:gallery_id>/', views_admin.edit_gallery, name='edit_gallery'),

    path('user/gallery/delete/<int:gallery_id>/', views_admin.delete_gallery, name='delete_gallery'),


    path('user/ingredient/list/<int:menu_item_id>/', views_admin.ingredient_list, name='ingredient_list'), 
    path('user/ingredient/add/<int:menu_item_id>/', views_admin.add_ingredient, name='add_ingredient'),
    path('user/ingredient/edit/<int:ingredient_id>/', views_admin.edit_ingredient, name='edit_ingredient'), 
    path('user/ingredient/delete/<int:ingredient_id>/', views_admin.delete_ingredient, name='delete_ingredient'),

     path('user/menu/list/', views_admin.list_menu_items, name='list_menu_items'),

    path('user/menu/add/', views_admin.add_menu_item, name='add_menu_item'),
    path('delete-image/<int:image_id>/', views_admin.delete_image, name='delete_image'),

    path('user/menu/edit/<int:menu_item_id>/', views_admin.edit_menu_item, name='edit_menu_item'),

    path('user/menu/delete/<int:menu_item_id>/', views_admin.delete_menu_item, name='delete_menu_item'),

    path('menu/pdf/<int:company_id>/', views_admin.generate_menu_pdf, name='generate_menu_pdf'),
    path('user/add-gallery-category/', views_admin.add_gallery_category, name='add_gallery_category'),
    path('user/edit-gallery-category/<int:category_id>/', views_admin.edit_gallery_category, name='edit_gallery_category'),
    path('user/delete-category/<int:category_id>/', views_admin.delete_gallery_category, name='delete_gallery_category'),
    path('user/list-gallery-categories/', views_admin.list_gallery_categories, name='list_gallery_categories'),





]

# Add media and static URLs in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
