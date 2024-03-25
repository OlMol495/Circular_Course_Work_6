import getpass

from django.conf import settings
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=settings.ROOT_EMAIL,
            first_name='Admin',
            last_name='Pro',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email_confirmed=True
        )

        user.set_password(settings.ROOT_PASSWORD)
        user.save()

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         email = input("Enter superuser email: ")
#
#         psw1 = getpass.getpass("Enter password: ")
#         psw2 = getpass.getpass("Confirm password: ")
#
#         while psw1 != psw2 or not psw1:
#             print("Passwords didn't match or empty!")
#             psw1 = getpass.getpass("Enter password: ")
#             psw2 = getpass.getpass("Confirm password: ")
#
#         user = User.objects.create(
#             email=email,
#             first_name="Admin",
#             last_name="Circular",
#             is_staff=True,
#             is_superuser=True,
#         )
#
#         user.set_password(psw1)
#         user.save()