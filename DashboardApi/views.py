import pandas as pd
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from DashboardApi.helpers.constants import *
from DashboardApi.helpers.exceptions import InvalidDataException
from DashboardApi.helpers.helper import pairwise
from indicators.models import Indicator
from regions.models import Panchayat, Block
from .serializers import HealthSerializer


# Create your views here.
# Posting data from excel file
# Health Report Upload
class HealthViewSet(ModelViewSet):
    serializer_class = HealthSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        file = request.FILES['health_sheet']
        df = pd.read_excel(file)
        print(df.columns)
        return Response(status=HTTP_SUCCESS)


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
        serializer = HealthSerializer(objs, many=True)
        return Response({"all_health_indicators": serializer.data})


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
    weightage = 0.0
    panchayat = Panchayat.objects.get(name='Patratu')
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
            weightage=weightage,
            block=block,
            panchayat=panchayat,
            numerator=num,
            denominator=den,
            percent=per,
            sector=_sector
        )
