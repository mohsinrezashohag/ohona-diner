from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import json

def home_admin(request):
    return render(request, 'backend/index.html')


#Contact Us
def add_contactus_admin(request):
    if request.method == 'POST':
        company_id = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if company_id and email and phone and address:
            try:
                company = Company.objects.get(id=company_id)

                # Check if a contact already exists for the company
                if ContactUs.objects.filter(company=company).exists():
                    messages.error(request, "Contact details for this company already exist.")
                else:
                    ContactUs.objects.create(
                        company=company,
                        email=email,
                        phone=phone,
                        address=address
                    )
                    messages.success(request, "Contact details added successfully!")
            except Company.DoesNotExist:
                messages.error(request, "Selected company does not exist.")
        else:
            messages.error(request, "All fields are required.")

    companies = Company.objects.all()
    return render(request, 'backend/contactus/contactus_add.html', {'companies': companies})



def contactus_admin(request):
    contacts = ContactUs.objects.select_related('company').all()
    return render(request, 'backend/contactus/contactus_list.html', {'contacts': contacts})




def edit_contactus_admin(request, contact_id):
    try:
        contact = ContactUs.objects.get(id=contact_id)
    except ContactUs.DoesNotExist:
        return JsonResponse({'success': False, 'message': "The contact does not exist."})

    if request.method == 'POST':
        company_id = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if company_id and email and phone and address:
            try:
                company = Company.objects.get(id=company_id)

                # Check if another contact exists for the selected company (excluding the current one)
                if ContactUs.objects.filter(company=company).exclude(id=contact_id).exists():
                    return JsonResponse({'success': False, 'message': "Contact details for this company already exist."})
                else:
                    contact.company = company
                    contact.email = email
                    contact.phone = phone
                    contact.address = address
                    contact.save()
                    return JsonResponse({'success': True, 'message': "Contact details updated successfully!"})

            except Company.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Selected company does not exist."})
        else:
            return JsonResponse({'success': False, 'message': "All fields are required."})

    companies = Company.objects.all()
    return render(request, 'backend/contactus/contactus_edit.html', {
        'contact': contact,
        'companies': companies
    })


def delete_contactus_admin(request, contact_id):

    contact = get_object_or_404(ContactUs, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        
        # Return a JSON response with a success message
        return JsonResponse({'success': True, 'message': 'Contact details deleted successfully!'})
    
    # Return a JSON response with an error message for unsupported methods
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



#Company 

def add_company(request):
    if request.method == 'POST':
        # Predefined list of companies to add
        company_names = ['Ohana Diner', 'Mini Malaysia', 'Sunny Side Up']
        
        # Check if the companies already exist
        existing_companies = Company.objects.filter(name__in=company_names)
        existing_company_names = existing_companies.values_list('name', flat=True)
        
        # Add the companies that don't exist
        for company_name in company_names:
            if company_name not in existing_company_names:
                # Handle the uploaded logo if present
                logo = request.FILES.get('logo')  # Get the logo from the form
                company = Company.objects.create(name=company_name, logo=logo)
                messages.success(request, f"{company_name} has been added successfully!")
        
        # Inform the user if companies are already in the database
        for company_name in company_names:
            if company_name in existing_company_names:
                messages.info(request, f"{company_name} already exists in the database.")
        
        return redirect('company_list')  # Redirect to the company list view
    
    return render(request, 'backend/company/add_company.html')


# Edit Company View
def edit_company(request, company_id):
    # Fetch the company object using the ID
    company = get_object_or_404(Company, id=company_id)
    
    if request.method == 'POST':
        # Get the form data
        new_name = request.POST.get('name')
        new_logo = request.FILES.get('logo')  # Get the new logo if uploaded
        
        # Update company details
        company.name = new_name
        
        if new_logo:
            company.logo = new_logo  # Update the logo if a new one is uploaded
        
        # Save the changes to the database
        company.save()
        
        # Add a success message
        messages.success(request, f"Company '{company.name}' has been updated successfully.")
        
        # Redirect to the company list page
        return redirect('company_list')
    
    # Render the form with the current company data
    return render(request, 'backend/company/edit_company.html', {'company': company})

# Delete Company View
def delete_company(request, company_id):
    if request.method == 'POST':
        company = get_object_or_404(Company, id=company_id)
        company_name = company.name
        
        # Optionally, delete the logo file from storage (if you want to free up space)
        if company.logo:
            # Delete the logo from the file system (unmanaged by Django)
            try:
                os.remove(company.logo.path)
            except Exception as e:
                print(f"Error removing logo: {e}")
        
        # Delete the company
        company.delete()
        return JsonResponse({'success': True, 'message': f"Company '{company_name}' has been deleted."})
    
    return JsonResponse({'success': False, 'message': 'Failed to delete company.'})


# Company List View (to show the list of companies)
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'backend/company/company_list.html', {'companies': companies})


def list_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        context = {
            "categories": categories
        }
        return render(request, "backend/category/list_categories.html", context)
    else:
        return render(request, "backend/category/error.html", {"message": "Invalid request method"})

def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        status = request.POST.get("status", True)
        image = request.FILES.get("image", None)

        if not name:
            return JsonResponse({"success": False, "message": "Name is required."}, status=400)

        category = Category.objects.create(
            name=name,
            description=description,
            status=bool(status),
            image=image
        )
        return JsonResponse({"success": True, "message": "Category added successfully.", "category_id": category.id})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)





    

def edit_category(request, category_id):
    if request.method == "POST":
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "Category not found."}, status=404)

        name = request.POST.get("name", category.name)
        description = request.POST.get("description", category.description)
        status = request.POST.get("status", category.status)
        image = request.FILES.get("image", category.image)

        category.name = name
        category.description = description
        category.status = bool(status)
        if image:
            category.image = image
        category.save()

        return JsonResponse({"success": True, "message": "Category updated successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def delete_category(request, category_id):
    if request.method == "DELETE":
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"success": True, "message": "Category deleted successfully."})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "Category not found."}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)



def list_galleries(request):
    if request.method == "GET":
        galleries = Gallery.objects.select_related('Gallerycategory').all()
        categories = Gallerycategory.objects.all()
        context = {
            "galleries": galleries,
            "categories": categories,
        }
        return render(request, "backend/gallery/list_galleries.html", context)
    else:
        return render(request, "backend/gallery/error.html", {"message": "Invalid request method"})




def add_gallery(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        image = request.FILES.get("image")
        status = request.POST.get("status", True)
        caption = request.POST.get("caption", "")

        if not category_id or not image:
            return JsonResponse({"success": False, "message": "Category and Image are required."}, status=400)

        category = get_object_or_404(Gallerycategory, id=category_id)

        gallery = Gallery.objects.create(
            Gallerycategory=category,
            image=image,
            status=bool(status),
            caption=caption
        )
        return JsonResponse({"success": True, "message": "Gallery added successfully.", "gallery_id": gallery.id})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)



def edit_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    category_id = request.POST.get('category_id')
    caption = request.POST.get('caption')
    status = request.POST.get('status')
    image = request.FILES.get('image')

    # Handle category
    try:
        category = Gallerycategory.objects.get(id=category_id)
    except Gallerycategory.DoesNotExist:
        return JsonResponse({"success": False, "message": "The selected category does not exist. Please select a valid category."})

    # Update gallery object
    gallery.category = category
    gallery.caption = caption
    gallery.status = status
    if image:
        gallery.image = image
    gallery.save()

    return JsonResponse({"success": True, "message": "Gallery updated successfully."})







def delete_gallery(request, gallery_id):
    if request.method == "DELETE":
        try:
            gallery = Gallery.objects.get(id=gallery_id)
            gallery.delete()
            return JsonResponse({"success": True, "message": "Gallery deleted successfully."})
        except Gallery.DoesNotExist:
            return JsonResponse({"success": False, "message": "Gallery not found."}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)



def list_gallery_categories(request):
    if request.method == "GET":
        categories = Gallerycategory.objects.all()
        context = {
            "categories": categories
        }
        return render(request, "backend/gallery/list_categories.html", context)
    else:
        return render(request, "backend/gallery/error.html", {"message": "Invalid request method"})

def add_gallery_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        status = request.POST.get("status", True)
        image = request.FILES.get("image", None)

        if not name:
            return JsonResponse({"success": False, "message": "Name is required."}, status=400)

        category = Gallerycategory.objects.create(
            name=name,
            description=description,
            status=bool(status),
            image=image
        )
        return JsonResponse({"success": True, "message": "Category added successfully.", "category_id": category.id})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)





    

def edit_gallery_category(request, category_id):
    if request.method == "POST":
        try:
            category = Gallerycategory.objects.get(id=category_id)
        except Gallerycategory.DoesNotExist:
            return JsonResponse({"success": False, "message": "Category not found."}, status=404)

        name = request.POST.get("name", category.name)
        description = request.POST.get("description", category.description)
        status = request.POST.get("status", category.status)
        image = request.FILES.get("image", category.image)

        category.name = name
        category.description = description
        category.status = bool(status)
        if image:
            category.image = image
        category.save()

        return JsonResponse({"success": True, "message": "Category updated successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def delete_gallery_category(request, category_id):
    if request.method == "DELETE":
        try:
            category = Gallerycategory.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"success": True, "message": "Category deleted successfully."})
        except Gallerycategory.DoesNotExist:
            return JsonResponse({"success": False, "message": "Category not found."}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)







# Add MenuItem
def add_menu_item(request):
    if request.method == "POST":
        # Get data from POST request
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = request.POST.get("price")
        category_id = request.POST.get("category_id")
        company_id = request.POST.get("company_id")
        hot_deal_status = request.POST.get("hot_deal_status", False) == "on"
        vat_tax = request.POST.get("vat_tax", 0)
        status = request.POST.get("status", False) == "on"
        
        # Save MenuItem
        category = get_object_or_404(Category, id=category_id)
        company = get_object_or_404(Company, id=company_id)
        
        # Handle Thumbnail Image (only single image)
        thumb_image = request.FILES.get("thumb_image")
        
        # Create the MenuItem object first
        menu_item = MenuItem.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            company=company,
            hot_deal_status=hot_deal_status,
            vat_tax=vat_tax,
            status=status,
            thumb_image=thumb_image,  # Save thumbnail image
        )
        
        # Handle multiple images (additional images)
        images = request.FILES.getlist("images")  # Get the list of files selected for additional images
        for image in images:
            MenuItemImage.objects.create(menu_item=menu_item, image=image)  # Save each image
        
        return redirect("list_menu_items")  # Replace with the correct URL name
    
    categories = Category.objects.all()
    companies = Company.objects.all()
    return render(request, "backend/menu/add_menu.html", {"categories": categories, "companies": companies})



# Edit MenuItem
def edit_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    if request.method == "POST":
        # Update fields from POST request
        menu_item.name = request.POST.get("name")
        menu_item.description = request.POST.get("description", "")
        menu_item.price = request.POST.get("price")
        menu_item.category = get_object_or_404(Category, id=request.POST.get("category_id"))
        menu_item.company = get_object_or_404(Company, id=request.POST.get("company_id"))
        menu_item.hot_deal_status = request.POST.get("hot_deal_status", False) == "on"
        menu_item.vat_tax = request.POST.get("vat_tax", 0.00)
        menu_item.status = request.POST.get("status", False) == "on"

        # Handle Thumbnail Image (if provided)
        thumb_image = request.FILES.get("thumb_image")
        if thumb_image:
            menu_item.thumb_image = thumb_image

        menu_item.save()

        # Handle multiple images (additional images)
        images = request.FILES.getlist("images")  # Multiple files
        for image in images:
            MenuItemImage.objects.create(menu_item=menu_item, image=image)

        return redirect("list_menu_items")  # Replace with the correct URL name
    
    # Fetch categories, companies, and existing additional images
    categories = Category.objects.all()
    companies = Company.objects.all()
    additional_images = menu_item.images.all()  # Using the related name "images"

    return render(
        request,
        "backend/menu/edit_menu.html",
        {
            "menu_item": menu_item,
            "categories": categories,
            "companies": companies,
            "additional_images": additional_images,
        },
    )



# Delete MenuItem
def delete_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    if request.method == "POST":
        menu_item.delete()
        return JsonResponse({"success": True, "message": "Menu item deleted successfully"})
    
    return render(request, "backend/menu/delete_menu.html", {"menu_item": menu_item})


# List Menu Items
def list_menu_items(request):
    menu_items = MenuItem.objects.all().select_related('category', 'company')
    return render(request, "backend/menu/list_menu.html", {"menu_items": menu_items})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  # If you're using AJAX POST requests, make sure CSRF is properly handled
def delete_image(request, image_id):
    if request.method == 'POST':
        # Attempt to fetch the image object by ID
        try:
            image = MenuItemImage.objects.get(id=image_id)  # Replace with your model for additional images
            image.delete()  # Delete the image from the database
            return JsonResponse({'success': True})
        except MenuItemImage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Image not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)



def ingredient_list(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    ingredients = Ingredient.objects.filter(menu_item=menu_item)
    
    return render(request, 'backend/ingredient/ingredient_list.html', {
        'menu_item': menu_item,
        'ingredients': ingredients
    })


def add_ingredient(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if name:
            # Create and save the new ingredient
            ingredient = Ingredient(menu_item=menu_item, name=name, quantity=quantity)
            ingredient.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Ingredient added successfully!',
                'ingredient': {
                    'id': ingredient.id,
                    'name': ingredient.name,
                    'quantity': ingredient.quantity,
                    

                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Name is required!'
            })

# Edit an existing ingredient (JSON response)
def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if name:
            # Update ingredient
            ingredient.name = name
            ingredient.quantity = quantity
            ingredient.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Ingredient updated successfully!',
                'ingredient': {
                    'id': ingredient.id,
                    'name': ingredient.name,
                    'quantity': ingredient.quantity
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Name is required!'
            })

# Delete an ingredient (JSON response)
def delete_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    menu_item_id = ingredient.menu_item.id
    ingredient.delete()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Ingredient deleted successfully!',
        'menu_item_id': menu_item_id
    })




def generate_menu_pdf(request, company_id):
    # Get the company and its menu items
    company = Company.objects.get(id=company_id)
    menu_items = MenuItem.objects.filter(company=company, status=True)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create a canvas object for the PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Define theme colors
    primary_color = colors.HexColor('#0066cc')  # Blue color for company name and borders
    secondary_color = colors.HexColor('#f2f2f2')  # Light grey background for sections

    # Add the company logo at the top of the menu card
    if company.logo:
        logo_path = company.logo.path
        pdf.drawImage(logo_path, 100, 750, width=200, height=100)

    # Set the title and style for the menu card
    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColor(primary_color)
    pdf.drawString(100, 720, f"{company.name} - Menu")

    # Add a line separator
    pdf.setStrokeColor(primary_color)
    pdf.setLineWidth(1)
    pdf.line(80, 705, 500, 705)

    # Set font for the menu items
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.black)

    # Start from a specific point on the page
    y_position = 680

    for item in menu_items:
        if y_position < 100:  # Check if space is left for more items, if not create new page
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750  # Reset y_position for the new page

        # Add the menu item name and price
        pdf.drawString(100, y_position, f"{item.name}")
        pdf.drawString(350, y_position, f"${item.price:.2f}")

        # Add the item description
        if item.description:
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawString(100, y_position - 15, f"Description: {item.description}")

        # Add the item image (if exists)
        item_images = MenuItemImage.objects.filter(menu_item=item)
        if item_images.exists():
            image_path = item_images.first().image.path  # Taking the first image
            pdf.drawImage(image_path, 420, y_position - 40, width=50, height=50)

        # Move down the page for the next item
        y_position -= 70  # Adjust this value to add space for the description and image

    # Close the PDF object and return the response
    pdf.showPage()
    pdf.save()

    # Get the PDF content from the buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    # Return the PDF as a downloadable response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{company.name}_menu.pdf"'
    return response



def login_admin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  # If user exists
            login(request, user)  # Log the user in
            print('User logged in: ', request.user.username)
            return redirect('home_admin')  # Redirect to the home_admin route
        else:
            messages.error(request, "Invalid username or password")  # Error message
    
    return render(request, 'backend/auth/login.html')  # Render login form for GET request


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login_admin')  # Redirect to the login page


def about_us_list(request):
    if request.user.is_authenticated:
        about_us_entries = AboutUs.objects.all()
        print('about_us_entries: ', about_us_entries)
        context = {
            'about_us_entries': about_us_entries,
        }

        if request.method == "POST":
            about_us_id = request.POST.get("id")
            title = request.POST.get("title")
            description = request.POST.get("description")
            image = request.FILES.get("image")

            about_us = get_object_or_404(AboutUs, id=about_us_id)
            about_us.title = title
            about_us.description = description

            if image:
                about_us.image = image

            about_us.save()
            messages.success(request, "About Us section updated successfully!")
            return redirect('about_us_list')
    
        return render(request, 'backend/about_us/about_us_list.html', context)
    
    else:
        return redirect('login_admin')



def about_us_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")  # This may now be None if no file is uploaded

        if title and description:  # Only validate required fields
            about_us = AboutUs(title=title, description=description, image=image)
            about_us.save()
            messages.success(request, f"{about_us.title} saved successfully!")
            return redirect('about_us_create')  # You may want to redirect to another page after saving
        else:
            messages.error(request, "Title and description are required!")
    return render(request, 'backend/about_us/about_us_create.html')



def about_us_update(request):
    if request.method == "POST":
        about_us_id = request.POST.get("id")
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        about_us = get_object_or_404(AboutUs, id=about_us_id)
        about_us.title = title
        about_us.description = description

        if image:
            about_us.image = image

        about_us.save()
        messages.success(request, "About Us section updated successfully!")
        return redirect('about_us_list')
    

def delete_about_us(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        delete_id_str = data.get('id')  # Retrieve the ID from the form
        print('delete id str: ', delete_id_str)
        delete_id = int(delete_id_str)

        print('delete id: ', delete_id)
        print('delete id type: ', type(delete_id))

        if delete_id:
            about_us_entry = get_object_or_404(AboutUs, id=delete_id)
            about_us_entry.delete()
            print('entry deleted successfully')
            return JsonResponse({'success': True})
        
        else:
            print('got an invalid id while deleting')
            return JsonResponse({'error': 'Invalid ID'})

    print('deleted got get request')
    return JsonResponse({'error': 'Invalid request'})


def company_profile_list(request):
    company_profiles = CompanyProfile.objects.all()
    companies = Company.objects.all()

    if request.method == "POST":
        company_profile_id = request.POST.get('id')
        company_id = request.POST.get('company_id')
        description = request.POST.get('description')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        facebook_link = request.POST.get('facebook')
        instagram_link = request.POST.get('instagram')
        linkedin_link = request.POST.get('linkedin')
        twitter_link = request.POST.get('twitter')
        tiktok_link = request.POST.get('tiktok')
        image = request.FILES.get("image")

        if company_profile_id and company_id and description:
            company = Company.objects.get(id=company_id)
            company_profile = get_object_or_404(CompanyProfile, id=company_profile_id)
            
            company_profile.company = company
            company_profile.description = description

            if email:
                company_profile.email = email

            if phone:
                company_profile.phone = phone

            if website:
                company_profile.website = website

            if address:
                company_profile.address = address

            if facebook_link:
                company_profile.facebook_link = facebook_link
            
            if instagram_link:
                company_profile.instagram_link = instagram_link

            if linkedin_link:
                company_profile.linkedin_link = linkedin_link

            if twitter_link:
                company_profile.twitter_link = twitter_link

            if tiktok_link:
                company_profile.tiktok_link = tiktok_link
            
            if image:
                company_profile.image = image

            company_profile.save()
            messages.success(request, "Company Profile section updated successfully!")
            return redirect('company_profile_list')

    context = {
        'companies': companies,
        'company_profiles': company_profiles
    }
    
    return render(request, 'backend/company_profile/company_profile_list.html', context)


def company_profile_create(request):
    companies = Company.objects.all()

    if request.method == "POST":
        company_id = request.POST.get('company_id')
        description = request.POST.get('description')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        facebook_link = request.POST.get('facebook')
        instagram_link = request.POST.get('instagram')
        linkedin_link = request.POST.get('linkedin')
        twitter_link = request.POST.get('twitter')
        tiktok_link = request.POST.get('tiktok')
        
        # Retrieve the image file
        image = request.FILES.get('image')

        # Save the company profile instance
        if company_id and description:
            company = Company.objects.get(id=company_id)

            company_profile = CompanyProfile.objects.create(
                company=company,
                description=description,
                email=email,
                phone=phone,
                website=website,
                address=address,
                facebook_link=facebook_link,
                instagram_link=instagram_link,
                linkedin_link=linkedin_link,
                twitter_link=twitter_link,
                tiktok_link=tiktok_link,
                image=image
            )

            messages.success(request, f"{company_profile.company.name} saved successfully!")
            return redirect('company_profile_create')
        
        else:
            messages.error(request, "Company name and description are required!")

    context = {
        'companies': companies
    }
    
    return render(request, 'backend/company_profile/company_profile_create.html', context)

def company_profile_delete(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        delete_id_str = data.get('id')  # Retrieve the ID from the form
        print('delete id str: ', delete_id_str)
        delete_id = int(delete_id_str)

        print('delete id: ', delete_id)
        print('delete id type: ', type(delete_id))

        if delete_id:
            about_us_entry = get_object_or_404(CompanyProfile, id=delete_id)
            about_us_entry.delete()
            print('entry deleted successfully')
            return JsonResponse({'success': True})
        
        else:
            print('got an invalid id while deleting')
            return JsonResponse({'error': 'Invalid ID'})

    print('deleted got get request')
    return JsonResponse({'error': 'Invalid request'})


def owner_profile_create(request):
    companies = Company.objects.all()

    if request.method == "POST":
        company_id = request.POST.get('company_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        facebook_link = request.POST.get('facebook')
        instagram_link = request.POST.get('instagram')
        linkedin_link = request.POST.get('linkedin')
        twitter_link = request.POST.get('twitter')
        
        # Retrieve the image file
        image = request.FILES.get('image')

        # Save the company profile instance
        if company_id and name:
            company = Company.objects.get(id=company_id)

            owner_profile = Owner.objects.create(
                company=company,
                name=name,
                description=description,
                email=email,
                phone=phone,
                facebook_link=facebook_link,
                instagram_link=instagram_link,
                linkedin_link=linkedin_link,
                twitter_link=twitter_link,
                image=image
            )

            messages.success(request, f"{owner_profile.name} saved successfully!")
            return redirect('owner_profile_create')
        
        else:
            messages.error(request, "Company name and description are required!")

    context = {
        'companies': companies
    }
    return render(request, 'backend/owner_profile/owner_profile_create.html', context)


def owner_profile_list(request):
    owner_profiles = Owner.objects.all()
    companies = Company.objects.all()

    if request.method == "POST":
        owner_profile_id = request.POST.get('id')
        company_id = request.POST.get('company_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        facebook_link = request.POST.get('facebook')
        instagram_link = request.POST.get('instagram')
        linkedin_link = request.POST.get('linkedin')
        twitter_link = request.POST.get('twitter')
        image = request.FILES.get("image")

        if owner_profile_id and company_id and name:
            company = Company.objects.get(id=company_id)
            owner_profile = get_object_or_404(Owner, id=owner_profile_id)
            
            owner_profile.company = company
            owner_profile.description = description

            if email:
                owner_profile.email = email

            if phone:
                owner_profile.phone = phone

            if address:
                owner_profile.address = address

            if facebook_link:
                owner_profile.facebook_link = facebook_link
            
            if instagram_link:
                owner_profile.instagram_link = instagram_link

            if linkedin_link:
                owner_profile.linkedin_link = linkedin_link

            if twitter_link:
                owner_profile.twitter_link = twitter_link
            
            if image:
                owner_profile.image = image

            owner_profile.save()
            messages.success(request, "Owner Profile section updated successfully!")
            return redirect('owner_profile_list')

    context = {
        'companies': companies,
        'owner_profiles': owner_profiles
    }
    
    return render(request, 'backend/owner_profile/owner_profile_list.html', context)


def owner_profile_delete(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        delete_id_str = data.get('id')  # Retrieve the ID from the form
        print('delete id str: ', delete_id_str)
        delete_id = int(delete_id_str)

        print('delete id: ', delete_id)
        print('delete id type: ', type(delete_id))

        if delete_id:
            about_us_entry = get_object_or_404(Owner, id=delete_id)
            about_us_entry.delete()
            print('entry deleted successfully')
            return JsonResponse({'success': True})
        
        else:
            print('got an invalid id while deleting')
            return JsonResponse({'error': 'Invalid ID'})

    print('deleted got get request')
    return JsonResponse({'error': 'Invalid request'})