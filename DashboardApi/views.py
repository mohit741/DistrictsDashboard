import pandas as pd
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from DashboardApi.helpers.exceptions import InvalidDataException
from DashboardApi.helpers.helper import pairwise
from indicators.models import Indicator
from regions.models import Block
from .serializers import IndicatorSerializer


# Posting data from excel file
class HealthUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        f = request.FILES['health_sheet']
        df = pd.read_excel(f)
        try:
            data, block = validate_data(df)
            create_model(data, block, 'Health')
        except InvalidDataException as e:
            print(e)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        objs = Indicator.objects.all()
        serializer = IndicatorSerializer(objs, many=True)
        return Response({"all_health_indicators": serializer.data})


class BlockWiseList(generics.ListAPIView):
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        queryset = Indicator.objects.all()
        sector = self.request.query_params.get('sector', None)
        block = self.request.query_params.get('block', None)
        serial = self.request.query_params.get('serial', None)
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        queryset = queryset.filter(sector=sector) if sector is not None else queryset
        queryset = queryset.filter(block__name=block) if block is not None else queryset
        queryset = queryset.filter(serial=serial) if serial is not None else queryset
        queryset = queryset.filter(created__year=year) if year is not None else queryset
        queryset = queryset.filter(created__month=month) if month is not None else queryset
        print(queryset)
        return queryset

# Check if the data is valid
def validate_data(df):
    data = {}
    cl = df.columns.dropna()
    keys = [i for i in cl if type(i) == float or type(i) == int]
    print(keys)
    df = df.iloc[4].dropna()
    block = df[0]
    values = [i for i in df if type(i) == int]
    # print(values)
    # print(len(keys))
    # print(len(values))
    if 2 * len(keys) != len(values):
        raise InvalidDataException
    vals = [[first, second] for first, second in pairwise(values)]
    for key, val in zip(keys, vals):
        # print('{} {} {}'.format(key, val[0], val[1]))
        mp = dict()
        mp[0] = val[0]
        mp[1] = val[1]
        data[key] = mp

    return data, block


# Create indicator using data from excel sheet
def create_model(data, _block, _sector):
    block = Block.objects.get(name=_block)
    for key in data:
        serial = str(key)
        num = data[key][0]
        den = data[key][1]
        per = float((float(num) / den) * 100)
        per = per if per <= 100.00 else 100.00
        # print(per)
        Indicator.objects.create(
            serial=serial,
            block=block,
            numerator=num,
            denominator=den,
            percent=per,
            sector=_sector,
            created='2019-05-01'
        )
