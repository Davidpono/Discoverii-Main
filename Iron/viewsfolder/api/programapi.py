from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from pymongo import MongoClient
from bson import ObjectId

class WorkoutAPIView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient('mongodb+srv://admin:root@cluster0.96vux8g.mongodb.net/?retryWrites=true&w=majority')

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()

    def get(self, request):
        # Use context manager for MongoDB client
        with self.client as client:
            db = client['Workouts']
            workouts_collection = db['Workouts']

            # Extract query parameters from the request
            id = request.query_params.get("id", '')
            days = request.query_params.get("Days", '')
            level = request.query_params.get("Levels", '')
            concentration = request.query_params.get('Concentration', '')
            goal = request.query_params.get('Goals', '')
            print("days", days, "level", level, "concentration", concentration, "goal", goal)

            # Build the query based on provided parameters
            query = {}

            if id and ObjectId.is_valid(id):
                query["_id"] = ObjectId(id)

            # Include conditions for other parameters if needed
            # Example: if days:
            #              query["Days"] = days
            if days:
                query["Days"] = days
            if level:
                query["Levels"] = level
            if concentration:
                query["Concentration"] = concentration
            if goal:
                query["Goals"] = goal

            workouts = list(workouts_collection.find(query))

            # Transform ObjectId to str for serialization
            for workout in workouts:
                workout['_id'] = str(workout['_id'])

            # Return the response
            return Response({"Workouts": workouts})

    def post(self, request):
        try:
            # Use context manager for MongoDB client
            with self.client as client:
                db = client['Workouts']  # Replace with your MongoDB database name
                workouts_collection = db['Workouts']  # Replace with your MongoDB collection name

                # Extract data from the request
                data = request.data

                # Insert the new workout into the MongoDB collection
                result = workouts_collection.insert_one(data)

                # Transform ObjectId to str for serialization
                workout_id = str(result.inserted_id)

                return Response({"message": "Workout added successfully", "workout_id": workout_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add other CRUD operations as needed (PUT, DELETE, etc.)
