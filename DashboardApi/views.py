import datetime
import random
from operator import itemgetter

import pandas as pd
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from DashboardApi.helpers.exceptions import InvalidDataException
from DashboardApi.helpers.helper import pairwise
from indicators.helpers.strings import health_indicators
from indicators.models import Indicator, Score
from regions.models import Block
from .serializers import IndicatorSerializer, BlockRankSerializer


# Posting data from excel file
class HealthUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        f = request.FILES['health_sheet']
        df = pd.read_excel(f)
        try:
            data, date, sector = validate_blockwise_data(df)
            create_model(data, date, sector)
            blocks = [_block for _block in data]
            month = datetime.datetime.strptime(date, '%Y-%m-%d').month
            year = datetime.datetime.strptime(date, '%Y-%m-%d').year
            calculate_score(blocks=blocks, month=month, year=year)
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
        # print(queryset)
        return queryset


class BlockWiseRankList(generics.ListAPIView):
    serializer_class = BlockRankSerializer

    def get_queryset(self):
        queryset = Score.objects.all()
        block = self.request.query_params.get('block', None)
        # serial = self.request.query_params.get('serial', None)
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        queryset = queryset.filter(block__name=block) if block is not None else queryset
        # queryset = queryset.filter(serial=serial) if serial is not None else queryset
        queryset = queryset.filter(period__year=year) if year is not None else queryset
        queryset = queryset.filter(period__month=month) if month is not None else queryset
        queryset = queryset.order_by('rank')
        # print(queryset)
        return queryset


# Check if the data is valid
def validate_blockwise_data(df):
    data = {}
    cl = df[df.columns[0]]
    keys = [i for i in df.columns if type(i) == float or type(i) == int]
    date = cl[0].strftime('%Y-%m-%d')
    # print(date)
    sector = df.columns[0]
    # print(sector)
    blocks = list(cl[4:])
    df = df.iloc[4:]
    rows = [df.iloc[i].dropna() for i in range(0, len(df))]
    for i in range(0, len(rows)):
        rows[i] = [j for j in rows[i] if type(j) == int]
        # print(rows[i])
    k = 0
    for i in blocks:
        data_inner = dict()
        values = rows[k]
        if 2 * len(keys) != len(values):
            raise InvalidDataException
        vals = [[first, second] for first, second in pairwise(values)]
        for key, val in zip(keys, vals):
            # print('{} {} {}'.format(key, val[0], val[1]))
            mp = dict()
            mp[0] = val[0]
            mp[1] = val[1]
            data_inner[key] = mp
        data[i] = data_inner
        k += 1
    # print(data)
    return data, date, sector


# Create indicator using data from excel sheet
def create_model(data, date, _sector):
    for _block in data:
        block = Block.objects.get(name=_block)
        # print(_block)
        print(date)
        for key in data[_block]:
            serial = str(key)
            num = random.randrange(1000, 5000)
            den = random.randrange(5001, 9999)
            # num = data[_block][key][0]
            # den = data[_block][key][1]
            per = float((float(num) / den) * 100)
            per = per if per <= 100.00 else 100.00
            # print('{} {} {} {}'.format(serial, num, den, per))
            Indicator.objects.create(
                serial=serial,
                block=block,
                numerator=num,
                denominator=den,
                percent=per,
                sector=_sector,
                created=date
            )


def calculate_score(blocks, sector, month, year):
    data = {}
    vals = {}
    for key in health_indicators:
        tmp = {}
        min, max, rnge = Indicator.get_serial_minmax(serial=key, month=month, year=year)
        tmp['min'] = float(min)
        tmp['max'] = float(max)
        tmp['range'] = float(rnge)
        # print('{} {} {}'.format(min, max, rnge))
        vals[key] = tmp
    queryset = Indicator.objects.filter(created__year=year, created__month=month)
    for block in blocks:
        blk = Block.objects.get(name=block)
        obj1 = queryset.filter(block=blk)
        cmp = 0.0
        total_weight = 0.0
        for key in health_indicators:
            obj2 = obj1.filter(serial=key).first()
            per = float(obj2.percent)
            cmp = cmp + health_indicators[key]['weight'] * ((per - vals[key]['min']) / vals[key]['range'])
            total_weight += health_indicators[key]['weight']
        data[block] = (cmp / total_weight)
    data_sorted = sorted(data.items(), key=itemgetter(1), reverse=True)
    rank = {}
    for i in range(0, len(data_sorted)):
        rank[data_sorted[i][0]] = i + 1
    # print(data)
    # print(rank)
    for block in blocks:
        Score.objects.create(
            composite=data[block],
            rank=rank[block],
            block=Block.objects.get(name=block),
            period=datetime.datetime(year, month, 1).strftime('%Y-%m-%d')
        )
