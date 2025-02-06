import json

from django.http import JsonResponse
from .db import db_ref
from game_logic.game_logic import TypeGame

# just for testing, need to delete when hosting
from django.views.decorators.csrf import csrf_exempt

try:
    game = TypeGame(db_ref)
    game.start_game()

except ValueError as e:
    game = None
    error_message = str(e)
except Exception as e:
    game = None
    error_message = f"Unexpected error during game setup: {str(e)}"


# just for testing, need to delete when hosting
@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body).get('user_input', None)

        if data:
            try:
                response_data = game.process_user_input(data)
                print(response_data)
                return JsonResponse(response_data, status=200)
            except ValueError as e:
                return JsonResponse({'error': f'Value error from database: {str(e)}'}, status=400, safe=False)
            except Exception as e:
                return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500, safe=False)
        else:
            return JsonResponse({'error': 'No user input provided'}, status=400, safe=False)

    return JsonResponse({'message': 'Please send a POST request'}, status=405, safe=False)