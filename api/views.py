from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import JsonResponse
import sys
from rest_framework.response import Response
import json


# Create your views here.
def convert_data(data):
    repre = data['representation']
    colors = [int(val) for val in data['color']]
    sat_op = data['operation']
    amount = int(data['amount'])
    return {'representation': repre, 'color': colors, 'operation': sat_op, 'amount': amount}


def check_valid(data):
    if data['representation'] != 'hsv':
        return False
    if not (0 <= data['color'][0] <= 360 and 0 <= data['color'][1] <= 100 and 0 <= data['color'][2] <= 100):
        return False
    if data['operation'] not in ['desaturate', 'saturate']:
        return False
    return True


@api_view(['GET', 'POST'])
def colorize(request):
    data = request.data
    converted_data = convert_data(data)
    if not check_valid(converted_data):
        return HttpResponse(status=404)
    # print(converted_data, file=sys.stderr)
    colors = converted_data['color']
    if converted_data['operation'] == 'desaturate':
        sat = colors[1]
        new_sat = max(int(sat - sat * converted_data['amount'] / 100), 0)
    elif converted_data['operation'] == 'saturate':
        sat = colors[1]
        new_sat = min(int(round(sat + sat * converted_data['amount'] / 100, 0)), 100)
    new_colors = colors.copy()
    new_colors[1] = new_sat
    new_data = {'representation': converted_data['representation'], 'color': colors,
                'operation': converted_data['operation'],
                'modified_color': new_colors}
    print(new_data, file=sys.stderr)
    return JsonResponse(new_data)
