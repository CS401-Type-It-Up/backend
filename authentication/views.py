from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.db import db_ref

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Check if username and password are provided
            if not username or not password:
                return JsonResponse({'message': 'Username and password cannot be empty'}, status=400)

            # Check if the username already exists in the database
            if db_ref.child('users').child(username).get():
                return JsonResponse({'message': 'Username already exists. Please choose another one'}, status=409)

            # Create a new user record in Firebase
            new_user = {
                'username': username,
                'password': password  # Consider hashing the password for security
            }
            db_ref.child('users').child(username).set(new_user)

            # Return success response
            return JsonResponse({'message': 'Signup successful!'}, status=201)

        except json.JSONDecodeError:
            # Return error if the request body is not valid JSON
            return JsonResponse({'message': 'Request body must be in JSON format'}, status=400)

        # Return 405 Method Not Allowed if the request method is not POST
    return JsonResponse({'message': 'Please send a POST request'}, status=405)

