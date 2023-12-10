import django

django.setup()
from apps.user.models import User
from apps.drone.models import DroneSettings

"""
Create a first user in the database
"""
user = User.objects.create_user(identifier="Nemesis", password="nemesis")
print('User Nemesis with password "nemesis" created')

"""
Create a drone settings in the database
"""
DroneSettings().save()
print("Drone settings created")

print("DB populated")
