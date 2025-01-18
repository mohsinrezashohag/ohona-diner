from django.shortcuts import render
from .models import *
from django.db.models import Min
from itertools import groupby
from twilio.rest import Client
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import ContactUs
import messagebird
from django.views.decorators.csrf import csrf_protect
from django.db.models import Prefetch
from django.utils.text import slugify
from itertools import zip_longest



def home(request):
    categories = Gallerycategory.objects.all().prefetch_related('galleries')
    
    hot_deal_items = MenuItem.objects.filter(hot_deal_status=True, status=True) \
    .select_related('company') \
    .prefetch_related('ingredients') \
    .order_by('-id')[:4]
    
    hot_deal_items_for = MenuItem.objects.filter(hot_deal_status=True, status=True) \
        .select_related('company') \
        .prefetch_related('ingredients')

    sorted_hot_deal_items = sorted(hot_deal_items_for, key=lambda x: x.company.name)

    grouped_hot_deals = {}
    for company, items in groupby(sorted_hot_deal_items, key=lambda x: x.company):
        grouped_hot_deals[company] = list(items)

    company_menu_with_ingredients = {}
    
    for company, menu_items in grouped_hot_deals.items():
        menu_item_chunks = [menu_items[i:i + 3] for i in range(0, len(menu_items), 3)]
        company_menu_with_ingredients[company] = menu_item_chunks
        
    return render(request, 'frontend/index.html', {
        'categories': categories,
        'hot_deal_items':hot_deal_items,
        'grouped_hot_deals': grouped_hot_deals,
        'company_menu_with_ingredients': company_menu_with_ingredients,
    })
# def menu_ohana(request):
#     try:
#         company = Company.objects.get(id=1)
        
#     except:
#         company = None

#     return render(request, 'frontend/menu_ohana.html')


# def menu_sunny_side_up(request):
#     return render(request, 'frontend/menu_sunny_side_up.html')


# def menu_mini_malaysia(request):
#     return render(request, 'frontend/menu_mini_malaysia.html')

def menu_items(request, company_slug, company_id):
    company = Company.objects.filter(id=company_id).first()
    company.slug_name = slugify(company.name)

    menu_items = MenuItem.objects.filter(company=company)
    hot_deal_menu_items = menu_items.filter(hot_deal_status=True)

    menu_items_query = MenuItem.objects.filter(company=company)
    
    categories_by_company = Category.objects.filter(
        id__in=menu_items_query.values_list('category_id', flat=True)
    )

    categories = categories_by_company.prefetch_related(
        Prefetch('menu_items', queryset=menu_items_query)
    )

    print('Total categories:', len(categories))
    print('All categories: ', categories)
    for category in categories:
        print('Category: ', category.name)

    if hot_deal_menu_items.exists():
        for hot_deal_menu_item in hot_deal_menu_items:
            hot_deal_menu_item.slug_name = slugify(hot_deal_menu_item.name)

    if menu_items.exists():
        for menu_item in menu_items:
            menu_item.slug_name = slugify(menu_item.name)

    for category in categories:
        for categoy_menu_item in category.menu_items.all():
            categoy_menu_item.slug_name = slugify(categoy_menu_item.name)


    print('menu_items: ', menu_items)
    print('hot_deal_menu_items: ', hot_deal_menu_items)

    context = {
        'company': company,
        'categories': categories,
        'menu_items': menu_items,
        'hot_deal_menu_items': hot_deal_menu_items,
    }
    
    return render(request, 'frontend/menu_items.html', context)


def about(request):
    about_us = AboutUs.objects.all()
    company_profiles = CompanyProfile.objects.all()
    # owners = Owner.objects.all()
    # Get unique owners based on email
    unique_owners = (
        Owner.objects.values('email')
        .annotate(min_id=Min('id'))
        .order_by('email')
    )
    
    # Fetch the full owner objects using the IDs of the unique emails
    owners = Owner.objects.filter(id__in=[owner['min_id'] for owner in unique_owners])

    print('about_us section: ', about_us)

    context = {
        'about_us': about_us,
        'company_profiles': company_profiles,
        'owners': owners,
    }

    return render(request, 'frontend/about.html', context)


def contact(request):
   
    contacts = ContactUs.objects.select_related('company').all()
    return render(request, 'frontend/contact.html', {'contacts': contacts})






def send_whatsapp_message(request):
    if request.method == "POST":
        name = request.POST.get('name')
        datepicker = request.POST.get('datepicker')
        timepicker = request.POST.get('timepicker')
        phone = request.POST.get('phone')
        company_id = request.POST.get('company')

        # Get the contact info for the selected company
        # contact_us = get_object_or_404(ContactUs, company_id=company_id)
        # recipient_phone = contact_us.phone  # Company contact number

        # Prepare WhatsApp message
        message_body = (
            f"Reservation Details:\n"
            f"Name: {name}\n"
            f"Date: {datepicker}\n"
            f"Time: {timepicker}\n"
            f"Phone: {phone}\n"
        )

        # Initialize MessageBird client (using the correct API key)
        client = messagebird.Client('45654ee4-970c-45cd-85ff-6dc83ec71784')  # Replace with your API key

        try:
            # Send WhatsApp message via MessageBird's messaging API
            message = client.message_create(
                originator='whatsapp:+8801958666961',  # Your WhatsApp sender number
                recipients=[f'whatsapp:{8801958666961}'],  # Recipient's WhatsApp number
                body=message_body
            )

            return JsonResponse({'success': True, 'message': 'Reservation sent via WhatsApp!'})

        except messagebird.client.ErrorException as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})



# def menu_single(request, menu_slug, company_id, menu_id):
#     company = Company.objects.filter(id=company_id).first()
#     menu_item = MenuItem.objects.filter(id=menu_id, company=company).first()

#     # categories = Category.objects.all()
#     if menu_item:
#         category = menu_item.category

#     context = {
#         'company': company,
#         'category': category,
#         'menu_item': menu_item
#     }
    
#     return render(request, 'frontend/menu_single.html', context)


def menu_single(request, menu_slug, company_id, menu_id):
    company = Company.objects.filter(id=company_id).first()
    menu_item = MenuItem.objects.filter(id=menu_id, company=company).first()
    
    if menu_item:
        menu_item.slug_name = slugify(menu_item.name)  # Assign temporary slug_name
        category = menu_item.category

        # Prepare menu items with slug_name
        menu_items_with_slugs = [
            {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'thumb_image': item.thumb_image,
                'slug_name': slugify(item.name),
            }
            for item in category.menu_items.all()
        ]
    else:
        menu_items_with_slugs = []
        category = None

    context = {
        'company': company,
        'category': category,
        'menu_item': menu_item,
        'menu_items_with_slugs': menu_items_with_slugs,  # Pass the new list
    }
    
    return render(request, 'frontend/menu_single.html', context)


def about(request):
    about_us = AboutUs.objects.all()
    company_profiles = CompanyProfile.objects.all()
    # owners = Owner.objects.all()
    # Get unique owners based on email
    unique_owners = (
        Owner.objects.values('email')
        .annotate(min_id=Min('id'))
        .order_by('email')
    )
    
    # Fetch the full owner objects using the IDs of the unique emails
    owners = Owner.objects.filter(id__in=[owner['min_id'] for owner in unique_owners])

    print('about_us section: ', about_us)

    context = {
        'about_us': about_us,
        'company_profiles': company_profiles,
        'owners': owners,
    }

    return render(request, 'frontend/about.html', context)