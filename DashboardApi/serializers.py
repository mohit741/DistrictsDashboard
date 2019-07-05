from rest_framework import serializers

from indicators.models import *


class IndicatorSerializer(serializers.ModelSerializer):
    block = serializers.CharField(source='get_block', max_length=50)
    indicator_name = serializers.CharField(source='get_indicator_name', max_length=300)
    numerator_name = serializers.CharField(source='get_num_name', max_length=300)
    denominator_name = serializers.CharField(source='get_den_name', max_length=300)

    class Meta:
        model = Indicator
        fields = '__all__'
