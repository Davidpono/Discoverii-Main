from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import random

class UserAPIView(APIView):
    def post(self, request):
        # Check the action based on the request path or data
        if request.path.endswith('register/'):
            return self.register_user(request)
        elif request.path.endswith('login/'):
            return self.login_user(request)
        else:
            return Response({"message": "Invalid endpoint"}, status=404)

    def register_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        uri = "mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["Iron"]
        collection = db["User"]

        data_to_insert = {
            "email": email,
            "password": password,
            "username": username,
        }

        try:
            result = collection.insert_one(data_to_insert)
            inserted_id = str(result.inserted_id)  # Convert ObjectId to string
            print("Inserted document ID:", inserted_id)
            return Response({"message": "User registered successfully", "inserted_id": inserted_id})
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Failed to register user"}, status=500)
        
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        uri = "mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["Users"]
        collection = db["Users"]

        query = {
            "email": email,
            "password": password,
        }

        try:
            user = collection.find_one(query)

            if user:
                print("Login successful. User data:", user)
                return Response({"message": "Login successful"})
            else:
                print("Login failed. User not found.")
                return Response({"message": "Login failed. User not found"}, status=401)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Internal Server Error"}, status=500)
