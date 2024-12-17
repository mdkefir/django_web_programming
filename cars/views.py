from typing import Any
from django.views.generic import TemplateView
from cars.models import Car
from django.http import JsonResponse
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class ShowCarsView(TemplateView):
    template_name = "cars/show_cars.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all()

        return context
    
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Вход пользователя через сессию
            return Response({
                'message': 'Успешный вход',
                'user': {
                    'username': user.username,
                    'is_staff': user.is_staff,
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
