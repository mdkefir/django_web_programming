from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/csrf/', views.get_csrf_token),
    path('api/auth/login/', views.login_view),
    path('api/auth/logout/', views.logout_view),
    path('api/auth/user/', views.get_user),
] 