from django.db import models

# Create your models here.
class Upload_audio(models.Model):
    display_audio = models.FileField()
    def __str__(self):
        return self.display_audio