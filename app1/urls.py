from django.urls import path
from . import views

urlpatterns = [
        # La URL raíz ('') redirige a la vista de login.
        path('', views.login_view, name='login'),
        path('registro/', views.registro_view, name='registro'),
        path('bienvenida/', views.bienvenida_view, name='bienvenida'),
        path('logout/', views.logout_view, name='logout'),
    ]