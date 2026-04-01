from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        USER           = 'user',           'User'
        BUSINESS_OWNER = 'business_owner', 'Business Owner'
        ADMIN          = 'admin',          'Admin'

    email    = models.EmailField(unique=True)
    phone    = models.CharField(max_length=20, blank=True)
    avatar   = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    role     = models.CharField(
                   max_length=20,
                   choices=Role.choices,
                   default=Role.USER
               )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_business_owner(self):
        return self.role == self.Role.BUSINESS_OWNER

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_staff

    def __str__(self):
        return f'{self.email} [{self.role}]'
