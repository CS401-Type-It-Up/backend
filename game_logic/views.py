import json
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    return render(request, 'index.html')

def play(request):
    difficulty = request.GET.get('difficulty', 'easy')
    return render(request, 'gameplay.html', {'difficulty': difficulty})

@csrf_exempt
@require_http_methods(["POST"])
def get_word_list(request):
    try:
        data = json.loads(request.body)
        level = data.get('level')
        num = data.get('num')

        if level and num:
            # For testing, return some sample words
            word_lists = {
                1: ["HELLO", "WORLD", "PYTHON", "DJANGO", "CODING"],
                2: ["REACT", "SWIFT", "KOTLIN", "JAVA", "RUST"],
                3: ["DOCKER", "LINUX", "CLOUD", "SERVER", "DATA"],
                4: ["NEURAL", "LEARN", "DEEP", "MIND", "BRAIN"]
            }
            
            words = word_lists.get(level, ["TEST", "WORD"])
            word_list = random.sample(words, min(num, len(words)))
            
            return JsonResponse({
                'words': word_list
            }, status=200)
        else:
            return JsonResponse({'error': 'No parameter provided'}, status=400)

    except Exception as e:
        print(f"Error in get_word_list: {str(e)}")
        return JsonResponse({
            'error': f'Server error: {str(e)}'
        }, status=500) 