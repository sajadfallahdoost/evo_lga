from django.db import models
from account.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.address_line1}"
