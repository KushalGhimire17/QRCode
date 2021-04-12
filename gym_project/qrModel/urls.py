from django.urls import path
from .views import qr_generator_view

urlpatterns = [
    path('', qr_generator_view, name='qr_generator')
]
