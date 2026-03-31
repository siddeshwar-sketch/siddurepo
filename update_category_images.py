import os
import shutil
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from campaigns.models import Category

# Define source images (absolute paths from artifacts)
# Note: These paths are from the model's perspective in the current turn
IMAGES = {
    'Medical': r'C:\Users\SURAJ MALIPATIL\.gemini\antigravity\brain\e79d8461-7531-480b-b944-d3dd50f49de9\medical_category_icon_1774941809976.png',
    'Education': r'C:\Users\SURAJ MALIPATIL\.gemini\antigravity\brain\e79d8461-7531-480b-b944-d3dd50f49de9\education_category_icon_1774941856558.png',
    'Animals': r'C:\Users\SURAJ MALIPATIL\.gemini\antigravity\brain\e79d8461-7531-480b-b944-d3dd50f49de9\animal_category_icon_1774941901022.png',
    'Environment': r'C:\Users\SURAJ MALIPATIL\.gemini\antigravity\brain\e79d8461-7531-480b-b944-d3dd50f49de9\environment_category_icon_1774941946361.png',
}

# Ensure destination directory exists
DEST_DIR = os.path.join('media', 'categories', 'icons')
os.makedirs(DEST_DIR, exist_ok=True)

for name, src_path in IMAGES.items():
    try:
        category = Category.objects.get(name=name)
        filename = f"{name.lower()}_icon.png"
        dest_path = os.path.join(DEST_DIR, filename)
        
        # Copy the file
        shutil.copy2(src_path, dest_path)
        
        # Update model (the string path relative to MEDIA_ROOT)
        category.icon = f"categories/icons/{filename}"
        category.save()
        print(f"Successfully updated image for {name}")
    except Category.DoesNotExist:
        print(f"Category {name} not found in database")
    except Exception as e:
        print(f"Error updating {name}: {e}")
