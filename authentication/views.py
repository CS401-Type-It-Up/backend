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
        # ============ Need to rework following the previous view format =========== #
        login_pass = False
        db_ref = Fetch_from_Firebase("users")
        users_data = db_ref.get()
        user = [usr for usr in users_data.values() if usr["username"] == userid ]  # Fetch the user based on the username
        if not user or passwd != str(user[0]['password']) : return Response({'message': 'The user id or password is incorrect. Login Denied!'}, status=401) # Validate the info
        return Response({'message': "Login Successfully!"}, status=200)

