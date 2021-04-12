from django.shortcuts import render
from .models import QRcode

# Create your views here.


def qr_generator_view(request):
    name = "Welcome to"
    obj = QRcode.objects.all()
    context = {
        'name': name,
        'obj': obj,
    }
    return render(request, 'qrModel/home.html', context)
