
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from django.shortcuts import render
from django.http import HttpResponse


import requests
import json
def login(request):
 
    return render(request, 'login.html')