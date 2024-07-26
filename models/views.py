from django.shortcuts import render, redirect
from django.views import View
import requests
from django.shortcuts import render


class IndexView(View):
    def get(self, request, barcode):
        url1 = f"http://165.232.40.190/api/v1/public/track/{barcode}/"
        response1 = requests.get(url1)
        data = response1.json()
        if len(data) != 0:
            check = data[0]['data']['checkpoints']
        else:
            check = []
        return render(request, 'login.html', {"comment": "Hello World", 'data': data, 'check': check})

