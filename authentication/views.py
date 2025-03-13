from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from authentication.game_user import GameUser


@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        num = data.get('num')

        if not username or not password:
            return Response({
                "success": False,
                'message': 'username and password cannot be empty'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not num:
            return Response({
                "success": False,
                'message': 'please provide number of words for each level'
            }, status=status.HTTP_400_BAD_REQUEST)

        new_user = GameUser(username=username, password=password)
        try:
            new_user.create(num)
        except (ValueError, KeyError, Exception) as e:
            return Response({
                "success": False,
                "message": str(e)
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

        current_user = GameUser(username=username, password=password)

        try:
            current_user.login()
        except (ValueError, KeyError, Exception) as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        progress = {
            "level": current_user.get_level(),
            "wordlist": current_user.get_wordlist(),
            "life": current_user.get_life(),
            "difficulty": current_user.get_difficulty(),
        }

        return Response({
            "success": True,
            "username": current_user.get_username(),
            "progress": progress,
            "message": "Login successful",
        })


@method_decorator(csrf_exempt, name='dispatch')
class SaveProgress(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        if not username:
            return Response({
                "success": False,
                'message': 'Missing username'
            }, status=status.HTTP_400_BAD_REQUEST)

        current_user = GameUser(username=username)

        try:
            current_user.save_progress(data)
        except (ValueError, KeyError, Exception) as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "Progress saved successfully"
        })


@method_decorator(csrf_exempt, name='dispatch')
class NextLevel(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        num = data.get('num')

        if not username:
            return Response({
                "success": False,
                'message': 'Missing username'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not num:
            return Response({
                "success": False,
                'message': 'Please provide the number of words for the new level'
            }, status=status.HTTP_400_BAD_REQUEST)

        current_user = GameUser(username=username)

        try:
            current_user.set_level(current_user.get_level() + 1)  # Increase the level
            current_user.create(num)  # Generate new word list for the new level
        except (ValueError, KeyError, Exception) as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "message": "User has successfully advanced to the next level",
            "level": current_user.get_level(),
            "wordlist": current_user.get_wordlist()
        })
