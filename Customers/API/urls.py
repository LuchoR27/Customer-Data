from django.urls import path

from API.views import index, download_csv, get_cities

urlpatterns = [
    path('', index, name="index"),
    path('csv/', download_csv, name="download_csv"),
    path('cities/', get_cities, name="get_cities")
]