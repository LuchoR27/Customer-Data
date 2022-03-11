import io
import csv
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from API.db_connector import MongoDB_Connector

db = MongoDB_Connector()


def index(request):
    return render(request, "index.html", {
        "provinces": db.get_provinces()
    })


def download_csv(request):
    headers = ["SCV_ID", "LEGAL_IDENTIFIER", "SCV_EMAIL_ADDRESS", "VALID_EMAIL_ADDRESS_FLAG", "SCV_PHONE1",
               "VALID_PHONE1_FLAG", "SCV_PHONE2", "VALID_PHONE2_FLAG", "SCV_PHONE3", "VALID_PHONE3_FLAG",
               "CUSTOMER_GENDER", "CUSTOMER_TITLE", "CUSTOMER_FORENAME", "CUSTOMER_SURNAME", "BIRTH_DATE", "ROAD_TYPE",
               "STREET", "NUM", "FLOOR", "CITY", "PROVINCE", "POSTAL_CODE"]
    if request.method == 'GET':
        city = request.GET.get('city')
        province = request.GET.get('province')
        query_params = {}
        if province:
            query_params['province'] = province
        if city:
            query_params['city'] = city
        qs = db.get_csv_data(**query_params)
        # Create CSV with queryset
        response = HttpResponse(content_type='text/csv')
        wr = csv.writer(response, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)
        for customer in qs:
            wr.writerow(customer.values())
        response['Content-Disposition'] = 'attachment; filename=data.csv'
        return response


def get_cities(request):
    if request.method == 'GET':
        province = request.GET.get('province')
        cities = list(db.get_cities_province(province))
        return JsonResponse(json.dumps(cities), safe=False)
