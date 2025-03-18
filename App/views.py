from django.shortcuts import render
from django.views.generic import TemplateView

class UserIndex(TemplateView):
    template_name = "index.html"