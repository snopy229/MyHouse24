from src.user.models import Role, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.roles(*args, **kwargs)
        self.create_is_staff(*args, **kwargs)

    def roles(self, *args, **kwargs):
        if Role.objects.exists():
            self.stdout.write(self.style.WARNING("Roles already initialized."))
            return
        roles = [
            {
                "title": "Управляющий",
            },
            {
                "title": "Бухгалтер",
            },
            {
                "title": "Электрик",
            },
            {
                "title": "Сантехник",
            },
            {
                "title": "Слесарь",
            },
        ]
        for role_data in roles:
            role, created = Role.objects.get_or_create(
                title=role_data["title"], defaults=role_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role.title}" created.'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Role "{role.title}" already exists.')
                )

    def create_is_staff(self, *args, **kwargs):
        if not User.objects.filter(is_staff=True).exists():
            User.objects.create_superuser(email="admin@gamil.com", password="admin")
