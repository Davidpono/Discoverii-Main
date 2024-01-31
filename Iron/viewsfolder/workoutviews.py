from django.http import JsonResponse
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import time

MAX_RETRIES = 3
RETRY_DELAY = 2

@csrf_exempt
def remove_underscore_from_id(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = key.lstrip('_') if key == '_id' else key
            new_dict[new_key] = remove_underscore_from_id(value)
        return new_dict
    elif isinstance(obj, list):
        return [remove_underscore_from_id(element) for element in obj]
    else:
        return obj

def retry_request(request_function, *args, **kwargs):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = request_function(*args, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt}: An error occurred during the request: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying after {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Max retries reached. Request failed.")
                raise

@csrf_exempt
def workout(request):
    if request.method == 'POST':
        if 'amount' in request.POST and 'level' in request.POST and 'concentration' in request.POST and 'goal' in request.POST:
            # This is the first form submission
            amount = request.POST['amount']
            level = request.POST['level']
            concentration = request.POST['concentration']
            goal = request.POST['goal']
            name = request.POST.get('name', '')
            
            print(f"Form 1 - Amount: {amount}, Level: {level}, Concentration: {concentration}, Goal: {goal}")
            
            url = 'https://discoveri.azurewebsites.net/api/workouts/'
            headers = {'Content-Type': 'application/json'}
            data = {
                "Days": amount,
                "Levels": level,
                "Concentration": concentration,
                "Goals": goal
            }
            
            try:
                # Make the GET request with query parameters using retry mechanism
                response = retry_request(requests.get, url, headers=headers, params=data)

                # Check the response
                if response.status_code == 200:
                    print("GET request successful!")
                    response_json = response.json()

                    # Check if 'Workouts' key is present in the response
                    if 'Workouts' in response_json:
                        # Iterate through each workout object and print its details
                        for workout in response_json['Workouts']:
                            print("Workout:")
                            for key, value in workout.items():
                                print(f"  {key}: {value}")
                    else:
                        print("No 'Workouts' key found in the response.")

                else:
                    print("Failed to get workouts.")
                    print("Status code:", response.status_code)
                    print("Response content:", response.text)
                    # Optionally, you can return a JsonResponse indicating success or failure
                    return render(request, 'workout.html')
                
                response_json['Workouts'] = remove_underscore_from_id(response_json['Workouts'])
                print("Modified Response JSON:", response_json)
                return render(request, 'workoutlist.html', {'response_json': response_json})

            except requests.RequestException as e:
                print(f"GET request failed after retries: {e}")
                # Optionally, you can return a JsonResponse indicating success or failure
                return render(request, 'workout.html')

        # Additional data from dynamically added sections
        else:
            input_data = {}

            for key, value in request.POST.items():
                # Check for keys that start with 'section'
                if key.startswith('section'):
                    section_id, field_type, form_counter = key.split('_')
                    days = section_id[-1]
                    section_data_list = input_data.get(section_id, [])
                    section_data = {}

                    if field_type in ['workoutname', 'intensity', 'sets', 'reps', 'url', 'comments', "dayname"]:
                        section_data[field_type] = value

                    section_data['days'] = days
                    section_data_list.append(section_data)
                    input_data[section_id] = section_data_list

            form2_days = request.POST.get('form2_days')
            form2_levels = request.POST.get('form2_levels')
            form2_concentration = request.POST.get('form2_concentration')
            form2_goals = request.POST.get('form2_goals')
            form2_ProgramName = request.POST.get('form2_ProgramName')

            print("Form 2 Data:")
            print("Days:", form2_days)
            print("Levels:", form2_levels)
            print("Concentration:", form2_concentration)
            print("Goals:", form2_goals)
            print("Program Name:", form2_ProgramName)
            print("Dynamically added section data:")
            print(input_data)

            base_url = 'https://discoveri.azurewebsites.net'
            endpoint = '/api/workouts/'

            # Replace 'your_api_key' with any required authentication headers
            transformed_data = {}

            for section_name, workouts in input_data.items():
                section_data = []
                current_workout = {}

                for parameter_dict in workouts:
                    parameter_name, value = next(iter(parameter_dict.items()))
                    if parameter_name == 'workoutname':
                        if current_workout:
                            section_data.append(current_workout)
                        current_workout = {'workoutname': value}
                    else:
                        current_workout[parameter_name] = value

                if current_workout:
                    section_data.append(current_workout)

                transformed_data[section_name] = section_data

            print("Transformed data:", transformed_data)

            data = {
                "Days": form2_days,
                "Levels": form2_levels,
                "Concentration": form2_concentration,
                "Goals": form2_goals,
                "Name": form2_ProgramName
            }

            new_transformed_data = {**data, **transformed_data}
            print("New JSON transformed data:", new_transformed_data)

            url = f'{base_url}{endpoint}'

            try:
                # Make the POST request using retry mechanism
                response = retry_request(requests.post, url, json=new_transformed_data)

                # Check the response
                if response.status_code == 200:
                    print('POST request successful')
                    print('Response:', response.json())
                    return render(request, 'goals.html')
                else:
                    print('POST request failed')
                    print('Status Code:', response.status_code)
                    print('Response:', response.text)
                    return render(request, 'goals.html')

            except requests.RequestException as e:
                print(f'POST request failed after retries: {e}')
                return render(request, 'goals.html')

    return render(request, 'workout.html')
