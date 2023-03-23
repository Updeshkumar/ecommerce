from django.urls import path
from rest_framework import routers
from .views import index

router = routers.DefaultRouter()

urlpatterns = [

    path('', index),
]