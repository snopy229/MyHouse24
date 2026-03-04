from src.user.models import Role, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.roles(*args, **kwargs)
        self.create_is_staff(*args, **kwargs)

    def roles(self, *args, **kwargs):
        role_titles = [
            "Директор",
            "Управляющий",
            "Бухгалтер",
            "Электрик",
            "Сантехник",
            "Слесарь",
        ]

        created_roles = {}

        for title in role_titles:
            role, created = Role.objects.get_or_create(title=title)
            created_roles[title] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{title}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Role "{title}" already exists.'))

    def create_is_staff(self, created_role, *args, **kwargs):
        if not User.objects.filter(is_staff=True).exists():
            director_role = created_role.get("Директор")

            User.objects.create_user(
                email="admin@gmail.com",
                password="admin",
                role=director_role,
                is_staff=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "Superuser 'admin@gmail.com' created with role 'Директор'."
                )
            )
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
