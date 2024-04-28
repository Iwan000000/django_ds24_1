from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email=os.getenv('SUPER_USER'),
            first_name="Admin",
            last_name="SkyPro",
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('SUPER_USER_PASS'))
        user.save()
