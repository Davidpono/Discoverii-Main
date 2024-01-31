from django.shortcuts import render
import copy
import requests

def actualworkoutview(request, section_param):
    try:
        # Retrieve the workout data using section_param
        print("actualworkoutview", section_param)
       
        url = 'https://discoveri.azurewebsites.net/api/workouts/'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "id": section_param,
        }

        # Make the GET request with query parameters
        response = requests.get(url, headers=headers, params=data)

        # Check the response
        if response.status_code == 200:
            print("GET request successful!")
            response_json = response.json()

            # Process the workout data
            try:
                modified_response = process_workout_data(response_json)
            except Exception as e:
                print("Error processing workout data:", str(e))
                return render(request, 'actualworkout.html', {'error_message': 'Error processing workout data'})

            # Pass the modified data to the template
            return render(request, 'actualworkout.html', {'response_json': modified_response})
        else:
            print("Failed to get workouts.")
            print("Status code:", response.status_code)
            print("Response content:", response.text)
            # Optionally, you can return a JsonResponse indicating success or failure
            return render(request, 'actualworkout.html', {'error_message': 'Failed to get workouts'})

    except requests.RequestException as req_exception:
        print("Request Exception:", str(req_exception))
        return render(request, 'actualworkout.html', {'error_message': 'Error in making the request to the API'})

    except Exception as general_exception:
        print("General Exception:", str(general_exception))
        return render(request, 'actualworkout.html', {'error_message': 'An unexpected error occurred'})

# Add other necessary imports and views here

import copy

def process_workout_data(workout_data):
    # Make a deep copy to avoid modifying the original data
    modified_data = copy.deepcopy(workout_data)

    # Iterate through each workout in 'Workouts'
    for workout in modified_data['Workouts']:
        # Create a list to store keys for removal
        keys_to_remove = []

        # Iterate through keys in the workout
        for key, value in workout.items():
            # Check if the key is a 'section' key and not 'sectionsection'
            if key.startswith('section') and key != 'sectionsection' and not key.startswith('sectionsection'):
                # Extract 'dayname' from the dynamic section
                dayname_value = workout[key][0].get('dayname', None)

                # Append 'dayname' to the corresponding dynamic section_section
                section_num = key[len('section'):]
                sectionsection_key = f'sectionsection{section_num}'

                # Check if 'sectionsection' key exists, if not, create it
                if sectionsection_key not in workout:
                    workout[sectionsection_key] = [{}]

                # Append 'dayname' to 'sectionsection'
                workout[sectionsection_key][0]['dayname'] = dayname_value

                # Add the 'section' key to the removal list
                keys_to_remove.append(key)

        # Remove keys that start with 'section' but not 'sectionsection'
        for key in keys_to_remove:
            workout.pop(key)

    return modified_data
