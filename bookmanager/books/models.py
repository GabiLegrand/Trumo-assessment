from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")  # Link to User

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)  # Assuming a 13-character ISBN
    creation_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.title