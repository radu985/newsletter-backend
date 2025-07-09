#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import CustomUser

# Check existing users
users = CustomUser.objects.all()
print(f"Total users: {users.count()}")
for user in users:
    print(f"User: {user.email} - {user.name} - Premium: {user.is_premium}")

# Create test user for API testing
test_email = "test@example.com"
try:
    test_user = CustomUser.objects.get(email=test_email)
    print(f"Test user already exists: {test_user.email}")
except CustomUser.DoesNotExist:
    test_user = CustomUser.objects.create_user(
        email=test_email,
        name="Test User",
        password="testpass123"
    )
    print(f"Created test user: {test_user.email} with password: testpass123")

print("\nYou can now test login with:")
print(f"Email: {test_email}")
print("Password: testpass123") 