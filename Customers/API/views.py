import io
import csv

from django.http import HttpResponse
from django.shortcuts import render

from API.db_connector import MongoDB_Connector

db = MongoDB_Connector()


def index(request):
    return render(request, "index.html", {
        "provinces": db.get_provinces(),
        "cities": db.get_cities()
    })


def download_csv(request):
    headers = ["SCV_ID", "LEGAL_IDENTIFIER", "SCV_EMAIL_ADDRESS", "VALID_EMAIL_ADDRESS_FLAG", "SCV_PHONE1",
               "VALID_PHONE1_FLAG", "SCV_PHONE2", "VALID_PHONE2_FLAG", "SCV_PHONE3", "VALID_PHONE3_FLAG",
               "CUSTOMER_GENDER", "CUSTOMER_TITLE", "CUSTOMER_FORENAME", "CUSTOMER_SURNAME", "BIRTH_DATE", "ROAD_TYPE",
               "STREET", "NUM", "FLOOR", "CITY", "PROVINCE", "POSTAL_CODE"]
    if request.method == 'GET':
        query_params = {}
        if request.GET.get('province'):
            query_params['province'] = request.GET.get('province')
        if request.GET.get('city'):
            query_params['city'] = request.GET.get('city')
        qs = db.get_csv_data(**query_params)
        # Create CSV with queryset
        buffer = io.StringIO()
        wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)
        for customer in qs:
            wr.writerow(customer.values())
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'
        return response
