from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.
class Landing(TemplateView):
    template_name = 'welcome.html'
