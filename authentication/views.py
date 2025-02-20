from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from config.db import db_ref
from authentication.models import GameUser

@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({
                "success": False,
                'message': 'Username and password cannot be empty'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        new_user = GameUser(username=username, password=password)
        try:
            new_user.create()
        except {ValueError, KeyError, Exception} as e:
            return Response({
                "success": False,
                "message": {e}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "User have been successfully created"
        })

@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({
                "success": False,
                'message': 'Username and password cannot be empty'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data = db_ref.child('users').child(username).get()

        if not user_data:
            return Response({
                "success": False,
                'message': 'Username does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        if user_data.get("password") != password:
            return Response({
                "success": False,
                'message': "Incorrect password"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Login successful",
        })