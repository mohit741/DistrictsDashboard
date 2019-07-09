from django.db import models
from django.db.models import Min, Max

from indicators.helpers.strings import health_indicators
from regions.models import Block, Panchayat


# Create your models here.
class Indicator(models.Model):
    serial = models.CharField(max_length=5)
    numerator = models.PositiveIntegerField()
    denominator = models.PositiveIntegerField()
    percent = models.DecimalField(max_digits=8, decimal_places=5)
    max = models.DecimalField(max_digits=8, decimal_places=5, default=0.00)
    sector = models.CharField(max_length=15)
    block = models.ForeignKey(Block, related_name='block', on_delete=models.CASCADE)
    created = models.DateField()

    def __str__(self):
        return self.block.name + '_' + self.sector + '_' + self.serial + '_' + self.created.strftime("%d/%m/%Y")

    @property
    def get_block(self):
        return self.block.name

    @property
    def get_percent(self):
        return self.percent

    @property
    def get_indicator_name(self):
        return health_indicators[self.serial]['name']

    @property
    def get_num_name(self):
        return health_indicators[self.serial]['num']

    @property
    def get_den_name(self):
        return health_indicators[self.serial]['den']

    @property
    def get_weight(self):
        return health_indicators[self.serial]['weight']

    @staticmethod
    def max_percent(serial, year, month):
        mx = Indicator.objects.filter(serial=serial, created__year=year, created__month=month).aggregate(
            max=Max('percent')
        )
        return mx['max']

    @staticmethod
    def get_serial_minmax(serial, month, year):
        indicators = Indicator.objects.filter(serial=serial, created__year=year, created__month=month).aggregate(
            min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        print(indicators['max'])
        print(indicators['min'])
        return indicators['min'], indicators['max'], rnge

    @staticmethod
    def get_panchayat_minmax(panchayat):
        indicators = Indicator.objects.filter(panchayat=panchayat).aggregate(min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        return indicators['min'], indicators['max'], rnge

    @staticmethod
    def get_block_minmax(block, month, year):
        indicators = Indicator.objects.filter(block=block, created__year=year, created__month=month).aggregate(
            min=Min('percent'), max=Max('percent'))
        rnge = indicators['max'] - indicators['min']
        return indicators['min'], indicators['max'], rnge


class Score(models.Model):
    composite = models.DecimalField(max_digits=7, decimal_places=3)
    rank = models.PositiveIntegerField()
    block = models.ForeignKey(Block, related_name='block_score', on_delete=models.CASCADE)
    period = models.DateField()

    def __str__(self):
        return self.block.name + '_' + self.period.strftime('%m-%Y')

    @property
    def get_block(self):
        return self.block.name

    @staticmethod
    def get_best(month, year):
        return Score.objects.get(rank=1, period__month=month, period__year=year)

    @staticmethod
    def get_worst(month, year):
        return Score.objects.get(rank=18, period__month=month, period__year=year)
