import django
django.setup()
from apps.user.models import User

"""
Create a first user in the database
"""
user = User.objects.create_user(
    identifier="Nemesis",
    password="nemesis"
)
print("User Nemesis with password \"nemesis\" created")
print("DB populated")
