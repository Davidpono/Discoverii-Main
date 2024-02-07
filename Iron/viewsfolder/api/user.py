import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId  # Import ObjectId from bson module

import random

class UserAPIView(APIView):
    def post(self, request):
        # Check the action based on the request path or data
        if request.path.endswith('register/'):
            return self.register_user(request)
        elif request.path.endswith('login/'):
            return self.login_user(request)
        elif request.path.endswith('user/'):
            return self.user_user(request)
        elif request.path.endswith('userworkouts/'):
            return self.userworkouts_user(request)
        elif request.path.endswith('updatebasic/'):
            return self.updatebasic_user(request)
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
        db = client["Iron"]
        collection = db["User"]

        query = {
            "email": email,
            "password": password,
        }

        try:
            user = collection.find_one(query)

            if user:
                user_id = str(user.get('_id'))  # Get the user ID
                print("Login successful. User data:", user)
                return Response({"message": "Login successful", "user_id": user_id})
            else:
                print("Login failed. User not found.")
                return Response({"message": "Login failed. User not found"}, status=401)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Internal Server Error"}, status=500)
    def user_user(self, request):
        user_id = request.data.get('user_id')  # Assuming you're passing the user's ObjectId as 'user_id'

        uri = "mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["Iron"]
        collection = db["User"]

        query = {
            "_id": ObjectId(user_id),  # Convert user_id to ObjectId
        }

        try:
            user = collection.find_one(query)

            if user:
                # Convert ObjectId to string before sending the response
                user['_id'] = str(user['_id'])
                # Remove the password field before sending the response
                user.pop('password', None)
                return Response({"message": "User data retrieved successfully", "user": user})
            else:
                print("User not found.")
                return Response({"message": "User not found"}, status=404)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Internal Server Error"}, status=500)
    def userworkouts_user(self, request):
        user_id = request.data.get('user_id')
        workout_id = request.data.get('id')
        workout_name = request.data.get('name')

        uri = "mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["Iron"]
        collection = db["User"]

        query = {
            "_id": ObjectId(user_id),
        }

        try:
            user = collection.find_one(query)

            if user:
                # If 'workouts' already exists, update it, otherwise add it
                if 'workouts' in user:
                    # Append new workout data to the existing workouts array
                    user['workouts'].append({"id": workout_id, "name": workout_name})
                else:
                    # Create a new 'workouts' field with the provided workout data
                    user['workouts'] = [{"id": workout_id, "name": workout_name}]

                # Update the user document in the database
                collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'workouts': user['workouts']}})
                
                return Response({"message": "Workout added successfully"})
            else:
                print("User not found.")
                return Response({"message": "User not found"}, status=404)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Internal Server Error"}, status=500)
    def updatebasic_user(self, request):
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        lastname = request.data.get('lastname')
        firstname = request.data.get('firstname')
        age = request.data.get('age')
        email = request.data.get('email')
        activeworkout = request.data.get('restdayMonday')
        restdaylist = request.data.get('restdaylist')

        uri = "mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["Iron"]
        collection = db["User"]

        query = {"_id": ObjectId(user_id)}
    
        print(restdaylist)
        try:
            existing_user = collection.find_one(query)

            if existing_user:
                # Prepare update data
                update_data = {}

                # Update only non-null fields
                if email is not None:
                    update_data["email"] = email
                if username is not None:
                    update_data["username"] = username
                if lastname is not None:
                    update_data["lastname"] = lastname
                if firstname is not None:
                    update_data["firstname"] = firstname
                if age is not None:
                    update_data["age"] = age
                if activeworkout is not None:
                    update_data["activeworkout"] = activeworkout
                if restdaylist is not None:
                    update_data["restdaylist"] = restdaylist
                # Update the existing user data
                if update_data:
                    collection.update_one(query, {"$set": update_data})
                    return Response({"message": "User data updated successfully"})
                else:
                    return Response({"message": "No data provided for update"}, status=400)
            else:
                return Response({"message": "User not found"}, status=404)
        except Exception as e:
            print("An error occurred:", e)
            return Response({"message": "Internal Server Error"}, status=500)