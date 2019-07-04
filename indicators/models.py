from django.db import models
from django.db.models import Min, Max

from indicators.helpers.strings import health_indicators
from regions.models import Block, Panchayat


# Create your models here.
class Indicator(models.Model):
    serial = models.CharField(max_length=5)
    weightage = models.DecimalField(max_digits=4, decimal_places=2)
    numerator = models.PositiveIntegerField()
    denominator = models.PositiveIntegerField()
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    sector = models.CharField(max_length=15)
    block = models.ForeignKey(Block, related_name='block', on_delete=models.CASCADE)
    panchayat = models.ForeignKey(Panchayat, related_name='panchayat', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.block.name + '_' + self.panchayat.name + ' ' + self.serial + '_' + self.created.strftime(
            "%d/%m/%Y, %H:%M:%S")

    @property
    def get_block(self):
        return self.block.name

    @property
    def get_panchayat(self):
        return self.panchayat.name

    @property
    def get_indicator_name(self):
        return health_indicators[self.serial]['name']

    @property
    def get_num_name(self):
        return health_indicators[self.serial]['num']

    @property
    def get_den_name(self):
        return health_indicators[self.serial]['den']

    @staticmethod
    def get_sector_minmax(sector):
        indicators = Indicator.objects.filter(sector=sector).aggregate(min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        return indicators['min'], indicators['max'], rnge

    @staticmethod
    def get_panchayat_minmax(panchayat):
        indicators = Indicator.objects.filter(panchayat=panchayat).aggregate(min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        return indicators['min'], indicators['max'], rnge

    @staticmethod
    def get_block_minmax(block):
        indicators = Indicator.objects.filter(block=block).aggregate(min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        return indicators['min'], indicators['max'], rnge
