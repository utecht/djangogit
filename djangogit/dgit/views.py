# Create your views here.
import os

from django.shortcuts import render_to_response


def index(request):
    """display the list of available git projects"""
    
    return render_to_response("index.html",
                              dict(name="World"))