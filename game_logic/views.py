import json
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from config.db import db_ref

def index(request):
    return render(request, 'index.html')

def play(request):
    difficulty = request.GET.get('difficulty', 'easy')
    return render(request, 'gameplay.html', {'difficulty': difficulty})

def gameplay(request):
    difficulty = request.GET.get('difficulty', 'easy')
    hearts = {
        'easy': 10,
        'medium': 7,
        'hard': 5
    }
    context = {
        'difficulty': difficulty,
        'hearts': hearts[difficulty]
    }
    return render(request, 'gameplay.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def get_word_list(request):
    try:
        data = json.loads(request.body)
        level = data.get('level')
        num = data.get('num')
        difficulty = data.get('difficulty', 'easy')  # Get difficulty from request

        if level and num:
            path = f"wordlists/level{level}"
            words = db_ref.child(path).get()

            if not words:
                return JsonResponse({
                    'error': f'No words available for Level {level}'
                }, status=404)

            word_list = random.sample(words, min(num, len(words)))
            hearts = {
                'easy': 10,
                'medium': 7,
                'hard': 5
            }

            return JsonResponse({
                'words': word_list,
                'hearts': hearts[difficulty]  # Send hearts count based on difficulty
            }, status=200)

        else:
            return JsonResponse({'error': 'No parameter provided'}, status=400)

    except Exception as e:
        print(f"Error in get_word_list: {str(e)}")
        return JsonResponse({
            'error': f'Server error: {str(e)}'
        }, status=500) 