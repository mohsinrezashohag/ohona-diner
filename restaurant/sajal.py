from .models import Company
from django.utils.text import slugify

def companies_processor(request):
    companies = Company.objects.all()

    for company in companies:
        # Ensure name is valid
        if company.name and company.name.strip():
            company.slug_name = slugify(company.name.strip())
            print(f"Warning: Company slug {company.slug_name } .")
        else:
            # Fallback for empty names
            company.slug_name = f"company-{company.id}"
            print(f"Warning: Company ID {company.id} has an invalid name.")

    return {'companies': companies}
