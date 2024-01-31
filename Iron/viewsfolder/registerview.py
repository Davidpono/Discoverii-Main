import requests
from django.shortcuts import render
import time

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        url = 'https://discoveri.azurewebsites.net/api/register/'
        headers = {'Content-Type': 'application/json'}

        data = {
            'email': email,
            'password': password,
            'username': username
        }

        max_retries = 3
        retry_delay = 2

        for _ in range(max_retries):
            try:
                # Send POST request to the registration API endpoint
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

                # Registration successful, check if inserted_id is present in the response
                response_json = response.json()
                inserted_id = response_json.get('inserted_id')

                if inserted_id:
                    print("Inserted document ID:", inserted_id)

                # Redirect the user or handle success as needed
                return render(request, 'userProfile.html', {'inserted_id': inserted_id})
            except requests.RequestException as e:
                # Handle connection errors, timeouts, or other request-related issues
                print(f"An error occurred during registration request: {e}")
                print("Response content:", response.content)
                print("Response headers:", response.headers)
                time.sleep(retry_delay)
        else:
            return render(request, 'register-login.html', {'error_message': 'Registration failed. Please try again.'})

    return render(request, 'register-login.html')
