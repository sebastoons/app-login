from django.urls import path
from . import views

urlpatterns = [
    # La URL raíz ('') redirige a la vista de login.
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('bienvenida/', views.bienvenida_view, name='bienvenida'),
    path('logout/', views.logout_view, name='logout'),
    # --- NUEVAS URLs PARA RECUPERACIÓN DE CONTRASEÑA ---
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('recuperar-confirmacion/', views.recuperar_confirmacion_view, name='recuperar_confirmacion'),
]