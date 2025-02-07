import json
import random

from django.http import JsonResponse
from .db import db_ref

# just for testing, need to delete when hosting
from django.views.decorators.csrf import csrf_exempt


# just for testing, need to delete when hosting
@csrf_exempt
def get_word_list(request):
    if request.method == 'POST':
        level = json.loads(request.body).get('level', None)
        num = int(json.loads(request.body).get('num', None))

        if level and num:
            try:
                path = f"levels/level{level}/words"
                words = db_ref.child(path).get()

                if not words:
                    raise ValueError(f"No words available for Level {level}.")

                word_list = random.sample(words, min(num, len(words)))
                print(f"Words loaded for Level {level}: {word_list}")

                return JsonResponse(word_list, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': f'Value error from database: {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'No parameter provided'}, status=400)

    return JsonResponse({'message': 'Please send a POST request'}, status=405, safe=False)
