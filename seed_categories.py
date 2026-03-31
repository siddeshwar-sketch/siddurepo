import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from campaigns.models import Category
from django.utils.text import slugify

def seed_categories():
    categories_data = [
        {'name': 'Medical', 'slug': 'medical'},
        {'name': 'Education', 'slug': 'education'},
        {'name': 'Emergency Relief', 'slug': 'emergency-relief'},
        {'name': 'Animal Welfare', 'slug': 'animal-welfare'},
        {'name': 'Environment', 'slug': 'environment'},
    ]

    print(f"Seeding {len(categories_data)} categories...")
    
    for cat_info in categories_data:
        obj, created = Category.objects.get_or_create(
            name=cat_info['name'],
            defaults={'slug': cat_info['slug']}
        )
        if created:
            print(f"Created category: {obj.name}")
        else:
            print(f"Category already exists: {obj.name}")

    print("Seeding complete!")

if __name__ == '__main__':
    seed_categories()
