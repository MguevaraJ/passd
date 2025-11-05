from django.db import models
from django.conf import settings

# Create your models here.

from utils.models import BaseModel

class Folder(BaseModel):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')

    def __str__(self):
        return self.name


class KeyItem(BaseModel):
    url = models.CharField(max_length=512)
    username = models.CharField(max_length=128)
    encrypted_pass = models.TextField()  # El frontend envía los datos ya encriptados
    note = models.TextField(blank=True)
    tags = models.CharField(max_length=256, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='key_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url} ({self.username})"
