from django.urls import path

from API.views import index, download_csv

urlpatterns = [
    path('', index, name="index"),
    path('csv/', download_csv, name="download_csv")
]