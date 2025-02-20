import json
import random

from django.http import JsonResponse
from .db import db_ref

# just for testing, need to delete when hosting
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# just for testing, need to delete when hosting
@csrf_exempt
@require_http_methods(["POST"])
def get_word_list(request):
    try:
        data = json.loads(request.body)
        level = data.get('level')
        num = data.get('num')

        if level and num:
            path = f"wordlists/level{level}"
            words = db_ref.child(path).get()

            if not words:
                return JsonResponse({
                    'error': f'No words available for Level {level}'
                }, status=404)

            word_list = random.sample(words, min(num, len(words)))
            
            # Add console.log to debug response
            print(f"Sending words to frontend: {word_list}")
            
            return JsonResponse({
                'words': word_list  # Make sure words are in this format
            }, status=200)
        else:
            return JsonResponse({'error': 'No parameter provided'}, status=400)

    except Exception as e:
        print(f"Error in get_word_list: {str(e)}")  # Debug log
        return JsonResponse({
            'error': f'Server error: {str(e)}'
        }, status=500)
