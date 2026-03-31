from campaigns.models import Category, Campaign

# Define the 4 target categories from the home page
categories_data = [
    ('Medical', 'medical'),
    ('Education', 'education'),
    ('Animals', 'animals'),
    ('Environment', 'environment')
]

for name, slug in categories_data:
    obj, created = Category.objects.get_or_create(
        slug=slug, 
        defaults={'name': name}
    )
    if created:
        print(f"Created category: {name} ({slug})")
    else:
        print(f"Category already exists: {name} ({slug})")

# Migrate campaigns from 'medical-emergency' to 'medical'
try:
    medical_cat = Category.objects.get(slug='medical')
    updated_count = Campaign.objects.filter(category__slug='medical-emergency').update(category=medical_cat)
    print(f"Updated {updated_count} campaigns from 'medical-emergency' to 'medical'.")
except Category.DoesNotExist:
    print("Error: 'medical' category not found.")

print("Category initialization complete.")
