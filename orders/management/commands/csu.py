
from django.contrib.auth.models import User
import os
from typing import Any
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создание суперпользователя"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        username: str = os.getenv("CAFE_SUPERUSER", "admin")
        password: str = os.getenv("CAFE_SUPERUSER_PASSWORD", "admin")

        if not username or not password:
            self.stdout.write(self.style.ERROR("Ошибка: Переменные окружения для суперпользователя не заданы."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Предупреждение: Суперпользователь '{username}' уже существует."))
        else:
            User.objects.create_superuser(username=username, email=None, password=password)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{username}' успешно создан."))
