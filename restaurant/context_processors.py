from .models import Company
from django.utils.text import slugify

def companies_processor(request):
    companies = Company.objects.all()

    # Add a slug_name attribute dynamically if needed
    for company in companies:
        company.slug_name = slugify(company.name)

    return {'companies': companies}