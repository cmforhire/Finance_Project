from .views import *
from django.urls import path

# define the different pages
urlpatterns = [
    path('', Landing.as_view(), name='home'),
]

