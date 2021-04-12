from django.urls import path, include
from .views import homepage_view, qr_generator_view


urlpatterns = [
    path('', homepage_view, name='join_gym'),
    path('qr_generate', qr_generator_view, name='qr_generate'),

]
