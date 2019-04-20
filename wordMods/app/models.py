from django.db import models

# Create your models here.
class recent(models.Model):
    word=models.CharField(max_length=20)
    result=models.CharField(max_length=25)

    def __str__(self):
        return self.name
