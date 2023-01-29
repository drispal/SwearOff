from django.db import models

LANGUAGE_CHOCIES = (
    ("fr", "Francais"),
    ("en", "English"),
)

# Create your models here.
class Audio(models.Model):
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOCIES, default="EN")
    audio = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)