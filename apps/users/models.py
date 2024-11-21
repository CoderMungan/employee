from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Kullanıcı yönetimi için özelleştirilmiş bir User Manager
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email adresi gerekli!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser is_staff=True olmalıdır.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser is_superuser=True olmalıdır.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Email ile giriş yapılacak bir kullanıcı modeli
    """

    USER_TYPE_CHOICES = (
        ("staff", "Personel"),
        ("admin", "Yetkili"),
    )
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="staff"
    )
    annual_leave_days = models.DecimalField(
        max_digits=5, decimal_places=2, default=14
    )  # Yıllık izin günleri
    monthly_work_hours = models.DecimalField(
        max_digits=6, decimal_places=2, default=0
    )  # Aylık çalışma saatleri
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Admin paneline erişim için gerekli
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Kullanıcı adı yerine email kullan
    REQUIRED_FIELDS = []  # Email dışında herhangi bir zorunlu alan yok

    def __str__(self):
        return self.email
