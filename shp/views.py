from django.shortcuts import render
from shp.models import Shp
from tiff.models import Tiff

# Create your views here.
def index(request):
    shp = Shp.objects.all()
    tiff = Tiff.objects.all()

    context = {
        'shp': shp,
        'tiff': tiff
    }
    
    return render(request, 'index.html', context)