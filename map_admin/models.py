from django.db import models

class Map(models.Model):
    name = models.CharField(max_length=255)

