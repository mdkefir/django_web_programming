from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
import json
import pyotp
import qrcode
from io import BytesIO
from django.core.cache import cache
import requests

@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})

@require_http_methods(["POST"])
@csrf_exempt  # Временно для отладки, потом уберем
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Требуются имя пользователя и пароль'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'username': user.username,
                'is_staff': user.is_staff,
            })
        else:
            return JsonResponse({'error': 'Неверные учетные данные'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt  # Временно для отладки, потом уберем
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Успешный выход из системы'})

@ensure_csrf_cookie
def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'username': request.user.username,
            'is_staff': request.user.is_staff,
        })
    return JsonResponse({'error': 'Не авторизован'}, status=401)

@require_http_methods(["POST"])
@csrf_exempt
def otp_login(request):
    try:
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Требуется авторизация'}, status=401)
            
        totp = pyotp.TOTP(request.user.profile.otp_key)
        success = totp.verify(data.get('key', ''))
        
        if success:
            cache.set(f'otp_good_{request.user.id}', True, timeout=300)
            
        return JsonResponse({'success': success})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def otp_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)
    
    otp_good = cache.get(f'otp_good_{request.user.id}', False)
    return JsonResponse({'otp_good': otp_good})

def otp_qr_code(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)
        
    if not hasattr(request.user, 'profile') or not request.user.profile.otp_key:
        return JsonResponse({'error': 'OTP не настроен'}, status=400)
        
    totp = pyotp.TOTP(request.user.profile.otp_key)
    provisioning_uri = totp.provisioning_uri(
        name=request.user.username,
        issuer_name="АвтоИнфо"
    )
    
    # Создаем QR-код
    qr = qrcode.make(provisioning_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    
    return HttpResponse(buffer, content_type="image/png")

def geocode_address(request):
    """Прокси для геокодирования адресов через Nominatim"""
    try:
        address = request.GET.get('address')
        if not address:
            return JsonResponse({'error': 'Address is required'}, status=400)

        # Проверяем кэш
        cache_key = f'geocode_{address}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)

        response = requests.get('https://nominatim.openstreetmap.org/search', params={
            'q': address,
            'format': 'json',
            'limit': 1
        }, headers={
            'User-Agent': 'AutoInfo/1.0'
        })
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                result = {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon'])
                }
                # Кэшируем результат на 24 часа
                cache.set(cache_key, result, 60 * 60 * 24)
                return JsonResponse(result)
            return JsonResponse({'error': 'Location not found'}, status=404)
        
        return JsonResponse({'error': 'Geocoding service error'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 