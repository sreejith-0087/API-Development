from django.urls import path
from . views import *


urlpatterns = [
    path('upload/', csv_file, name='upload-csv'),
    path('', upload_view, name='csv_file'),
    path('saved-records/', saved_records_view, name='saved-records'),

]

