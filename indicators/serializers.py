from rest_framework import serializers

from regions.models import *
from .models import *


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block


class PanchayatSerializer(serializers.ModelSerializer):
    # block = BlockSerializer()

    class Meta:
        model = Panchayat


class IndicatorSerializer(serializers.ModelSerializer):
    # block = BlockSerializer()
    # panchayat = PanchayatSerializer()

    class Meta:
        model = Indicator
        read_only_fields = ('created',)
