from rest_framework.decorators import api_view
from django.http import JsonResponse
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from django.http import HttpResponse
import sys


def check_modified_valid(data):
    if data['representation'] != 'hsv':
        return False
    if not (0 <= data['color'][0] <= 360 and 0 <= data['color'][1] <= 100 and 0 <= data['color'][2] <= 100):
        return False
    if data['operation'] not in ['desaturate', 'saturate']:
        return False
    return True


@api_view(['GET', 'POST'])
def modify_color(request):
    if request.method == 'POST':
        data = request.data
        if not check_modified_valid(data):
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        # print(data, file=sys.stderr)
        colors = data['color']
        if data['operation'] == 'desaturate':
            sat = colors[1]
            new_sat = max(int(sat - sat * data['amount'] / 100), 0)
        elif data['operation'] == 'saturate':
            sat = colors[1]
            new_sat = min(int(round(sat + sat * data['amount'] / 100, 0)), 100)
        new_colors = colors.copy()
        new_colors[1] = new_sat
        new_data = {'representation': data['representation'], 'color': colors,
                    'operation': data['operation'],
                    'modified_color': new_colors}
        # print(new_data, file=sys.stderr)
        return JsonResponse(new_data)
    else:
        return JsonResponse({})


def check_valid(data):
    if set(data.keys()) != {'representation', 'color', 'conversion'}:
        return False
    if data['representation'] not in ['hsv', 'rgb']:
        return False
    if data['conversion'] not in ['rgb', 'hsv']:
        return False

    if data['representation'] == 'hsv':
        if not (0 <= data['color'][0] <= 360 and 0 <= data['color'][1] <= 100 and 0 <= data['color'][2] <= 100):
            return False

    if data['representation'] == 'rgb':
        if not (0 <= data['color'][0] <= 255 and 0 <= data['color'][1] <= 255 and 0 <= data['color'][2] <= 255):
            return False

    return True


@api_view(['GET', 'POST'])
def convert_color(request):
    if request.method == 'POST':
        data = request.data

        print('----', file=sys.stderr)
        if not check_valid(data):
            print('invalid', file=sys.stderr)
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        print(data, file=sys.stderr)
        colors = data['color']
        if data['representation'] == 'hsv' and data['conversion'] == 'rgb':
            new_colors = (hsv_to_rgb([colors[0] / 360, colors[1] / 100, colors[2] / 100]) * [255, 255, 255]).round(0)
        if data['representation'] == 'rgb' and data['conversion'] == 'hsv':
            new_colors = (rgb_to_hsv([colors[0] / 255, colors[1] / 255, colors[2] / 255]) * [360, 100, 100]).round(0)
        new_data = {'color': colors, 'converted_color': list(new_colors)}
        print(new_data, file=sys.stderr)
        return JsonResponse(new_data)
    else:
        return JsonResponse({})
