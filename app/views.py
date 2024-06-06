from django.shortcuts import render
from django.http import JsonResponse
from app.model import rate_answer, get_bot_response

def home(request):
    return render(request, 'index.html')

def get_response(request):
    if request.method == 'POST':
        user_text = request.POST.get('msg')
        response = get_bot_response(user_text)
        rating = rate_answer(user_text)
        return JsonResponse({"response": response, "rating": rating})