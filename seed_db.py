import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_care_management.settings')
django.setup()

from bookings.models import Service
from accounts.models import User

def seed():
    # 1. Create Default Services
    services = [
        {"name": "General Checkup", "description": "Basic health checkup and consultation", "price": 500.00},
        {"name": "Vaccination", "description": "Annual vaccines and shots", "price": 800.00},
        {"name": "Grooming", "description": "Full bath, hair trim, and nail clipping", "price": 1200.00},
        {"name": "Surgery", "description": "Minor to major surgical procedures", "price": 5000.00},
        {"name": "Dental Cleaning", "description": "Professional teeth cleaning", "price": 1500.00},
    ]
    
    print("Seeding services...")
    for s_data in services:
        obj, created = Service.objects.get_or_create(name=s_data['name'], defaults=s_data)
        if created:
            print(f"Created service: {obj.name}")
        else:
            print(f"Service exists: {obj.name}")
            
    # 2. Create Default Admin
    print("Checking for admin user...")
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@vetsphere.com',
            password='adminpassword123'
        )
        print("Superuser created! Username: admin | Password: adminpassword123")
    else:
        print("Superuser already exists.")

if __name__ == '__main__':
    seed()
    print("Database seeding completed.")
