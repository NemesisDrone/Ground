import django

django.setup()

"""
For every model we clear the database before populating it
"""

"""
Create a first user in the database
"""
from apps.user.models import User
User.objects.all().delete()
user = User.objects.create_user(identifier="Nemesis", password="nemesis")
print('User Nemesis with password "nemesis" created')

"""
Create a drone settings in the database
"""
from apps.drone.models import DroneSettings
DroneSettings.objects.all().delete()
DroneSettings().save()
print("Drone settings created")

print("DB populated")
