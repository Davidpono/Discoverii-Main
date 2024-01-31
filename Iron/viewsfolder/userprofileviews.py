
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from django.shortcuts import render
from django.http import HttpResponse


import requests
import json
def userprofile(request, inserted_id=None):
        print(f"Received inserted_id: {inserted_id}")

        return render(request, 'userProfile.html')