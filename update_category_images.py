import os
import shutil
import django
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from campaigns.models import Category

# Source paths (from the brain directory)
brain_dir = r"C:\Users\ADMIN\.gemini\antigravity\brain\df129f98-9378-4e24-8bb5-b3d34ba4af66"
media_dir = os.path.join(os.getcwd(), 'media', 'categories', 'icons')

# Create media directory if it doesn't exist
os.makedirs(media_dir, exist_ok=True)

# Map category slugs to their newly generated image filenames
image_map = {
    'medical': 'cat_medical_1774979280198.png',
    'education': 'cat_education_17749318829.png', # Wait, let me double check filenames
    'emergency-relief': 'cat_emergency_1774979409037.png',
    'animal-welfare': 'cat_animal_1774979622650.png',
    'environment': 'cat_environment_1774979674531.png'
}

# Correcting education filename (I saw 1774979318829 in previous step)
image_map['education'] = 'cat_education_1774979318829.png'

for slug, filename in image_map.items():
    src = os.path.join(brain_dir, filename)
    dst_filename = f"{slug}.png"
    dst = os.path.join(media_dir, dst_filename)
    
    if os.path.exists(src):
        # Move file to media directory
        shutil.copy(src, dst)
        print(f"Moved {filename} to {dst}")
        
        # Update Database
        try:
            cat = Category.objects.get(slug=slug)
            cat.icon = f"categories/icons/{dst_filename}"
            cat.save()
            print(f"Updated database for category: {cat.name}")
        except Category.DoesNotExist:
            print(f"Category with slug {slug} not found in DB.")
    else:
        print(f"Source file not found: {src}")

print("Category image update complete!")
