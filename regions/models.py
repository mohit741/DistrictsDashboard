from django.db import models


# Create your models here.
class Block(models.Model):
    name = models.CharField(max_length=50)
    district = models.CharField(max_length=50, default='Ranchi')
    lng = models.DecimalField(max_digits=8, decimal_places=5, default=0.0)
    lat = models.DecimalField(max_digits=8, decimal_places=5, default=0.0)

    def __str__(self):
        return self.name


class Panchayat(models.Model):
    name = models.CharField(max_length=50)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='block_name')

    def __str__(self):
        return self.name
