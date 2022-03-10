from django.shortcuts import render

from API.db_connector import MongoDB_Connector

db = MongoDB_Connector()


def index(request):
    return render(request, "index.html", {
        "provinces": db.get_provinces(),
        "cities": db.get_cities()
    })


def download_csv(request):
    pass
