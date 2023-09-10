# models.py
from django.db import models

class ScannedIDCard(models.Model):
    image = models.ImageField(upload_to='scanned_images/')
    id_card_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
