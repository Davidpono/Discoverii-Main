import math
import pandas as pd
import pymongo
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, OperationalError
from pymongo import MongoClient
from pymongo.server_api import ServerApi 
from ..models import User
import requests
import json
# Create your views here.
def goal (request):
    return render(request,"goals.html")
def pick_meals(meal_lists, target_calories):
    best_combo = None
    closest_calories = float('inf')

    for combo in zip(*meal_lists):
        total_calories = sum(item['calories'] for item in combo)
        
        if abs(total_calories - target_calories) < abs(closest_calories - target_calories):
            best_combo = combo
            closest_calories = total_calories

    return best_combo

def bbing(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        waist = request.POST.get('waist')
        neck = request.POST.get('neck')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        hip = request.POST.get('hip')  # Assuming you have a 'hip' input field
        
        # Validate and handle None values
        if not all([waist, neck, height, weight, age]):
            response_text = "Please provide all required measurements."
            return HttpResponse(response_text)

        waist = float(waist)
        neck = float(neck)
        height = float(height)
        weight = float(weight)
        age = float(age)
        gender = 'male'
        if gender == 'male':
            bfp = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
        elif gender == 'female':
            if hip:
                hip = float(hip)
                if waist > neck:
                    bfp = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450
                else:
                    bfp = 495 / (1.29579 - 0.35004 * math.log10(waist - neck) + 0.22100 * math.log10(height)) - 450
            else:
                response_text = "Please provide hip measurement for female calculation."
                return HttpResponse(response_text)
        else:
            response_text = "Invalid gender selection."
            return HttpResponse(response_text)
        
        # Calculate BMR using the provided formula
        bmr = 370 + 21.6 * (1 - bfp/100 ) * weight
        breakfast = [
            ["Oatmeal with Berries", 300, 5, 10, 50],
            ["Scrambled Eggs with Spinach", 500, 15, 25, 50],
            ["Grilled Chicken with Broccoli", 400, 10, 50, 20],
            ["Greek Yogurt with Nuts", 150, 8, 10, 20],
            ["Whole Wheat Pancakes with Fruit", 350, 5, 8, 70],
            ["Avocado Toast with Eggs", 450, 15, 20, 30],
            ["Smoothie Bowl with Granola", 350, 8, 12, 60],
            ["Cottage Cheese and Fruit", 250, 5, 15, 40],
            ["Peanut Butter Banana Toast", 300, 8, 10, 45],
            ["Veggie Omelette", 350, 10, 20, 30]
        ]

        lunch = [
            ["Grilled Chicken Salad", 400, 15, 30, 20],
            ["Quinoa and Vegetable Stir-Fry", 550, 8, 15, 60],
            ["Salmon with Asparagus", 450, 20, 40, 15],
            ["Hummus and Veggie Wrap", 300, 12, 10, 40],
            ["Turkey and Avocado Wrap", 350, 10, 20, 40],
            ["Bean and Vegetable Soup", 250, 5, 8, 45],
            ["Chicken Caesar Wrap", 400, 12, 25, 40],
            ["Grilled Cheese with Tomato Soup", 450, 15, 20, 60],
            ["Chickpea Salad", 350, 8, 10, 45],
            ["Sushi Roll with Brown Rice", 500, 10, 20, 80]
        ]

        dinner = [
            ["Baked Sweet Potato with Turkey", 350, 10, 25, 40],
            ["Steak with Roasted Vegetables", 600, 18, 40, 50],
            ["Grilled Fish Tacos", 450, 15, 30, 30],
            ["Vegetable Curry with Rice", 400, 10, 10, 70],
            ["Pasta Primavera", 500, 12, 15, 80],
            ["Chicken Stir-Fry with Brown Rice", 550, 15, 30, 45],
            ["Stuffed Bell Peppers", 350, 10, 20, 30],
            ["Spaghetti Squash with Marinara", 300, 8, 5, 60],
            ["Teriyaki Chicken with Broccoli", 450, 15, 25, 40],
            ["Lentil and Vegetable Stew", 300, 5, 10, 50]
        ]

        snacks1 = [
            ["Apple with Peanut Butter", 200, 10, 4, 25],
            ["Mixed Nuts", 250, 20, 6, 10],
            ["Yogurt Parfait", 180, 3, 8, 30],
            ["Cheese and Whole Grain Crackers", 180, 8, 5, 15],
            ["Rice Cakes with Almond Butter", 150, 6, 3, 20],
            ["Hard-Boiled Eggs", 140, 10, 12, 1],
            ["Veggie Sticks with Hummus", 150, 5, 3, 20],
            ["Trail Mix", 200, 12, 4, 20],
            ["Greek Yogurt with Honey", 160, 5, 10, 20],
            ["Turkey Jerky", 100, 2, 15, 4]
        ]

        snacks2 = [
            ["Carrot Sticks with Hummus", 150, 5, 3, 20],
            ["Protein Shake", 220, 2, 25, 10],
            ["Cottage Cheese with Fruit", 180, 3, 15, 20],
            ["Trail Mix", 200, 12, 4, 30],
            ["Greek Yogurt with Honey", 160, 5, 10, 15],
            ["Rice Crackers with Sliced Cheese", 130, 6, 3, 15],
            ["Fruit Salad", 120, 1, 1, 30],
            ["Almonds", 100, 8, 4, 4],
            ["Rice Cakes with Nutella", 150, 4, 2, 20],
            ["Chocolate Protein Bar", 200, 8, 15, 20]
]
        
        meal_lists = [breakfast, lunch, dinner, snacks1, snacks2]

        # Calculate target calories
        target_calories = bmr  # Use BMR as the target calories

        # Initialize variables to store best combination and closest calories
        best_combo = None
        closest_calories = float('inf')

        # Iterate through all possible combinations of meals
        for combo in zip(*meal_lists):
            total_calories = sum(item[1] for item in combo)  # Use index 1 to access calories

            # Check if the current combination is closer to the target
            if abs(total_calories - target_calories) < abs(closest_calories - target_calories):
                best_combo = combo
                closest_calories = total_calories

        # Print the selected meals
        response_meals = []
        for meal in best_combo:
            meal_name = meal[0]  # Use index 0 to access meal name
            meal_calories = meal[1]  # Use index 1 to access calories
            meal_carbs = meal[2]  # Use index 2 to access carbs
            meal_protein = meal[3]  # Use index 3 to access protein
            meal_fats = meal[4]
            response_meals.append(
                f"Selected Meal: {meal_name}\nCalories: {meal_calories}\nCarbs: {meal_carbs}\nProtein: {meal_protein}\Fats: {meal_fats}\n"
            )

        # Create response text
        response_text = f"Gender: {gender}\nBody Fat Percentage: {bfp:.2f}%\nBMR: {bmr:.2f} calories/day\n\nSelected Meals:\n"
        response_text += "\n".join(response_meals)
        return HttpResponse(response_text)
    
    return render(request, 'bodyboulding.html')


