from django.db import models

# Create your models here.
class Image(models.Model):
        phrase = models.CharField(max_length=2000)
        ai_image=models.ImageField(upload_to='images')

        def __str__(self):
                return str(self.phrase)