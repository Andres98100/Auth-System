from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Access_Code(models.Model):
    code = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una instancia nueva (aún no ha sido guardada en la base de datos)
            self.created_at = timezone.now()  # Establece created_at en el momento actual
        self.expires_at = self.created_at + timedelta(minutes=15)
        super(Access_Code, self).save(*args, **kwargs)
