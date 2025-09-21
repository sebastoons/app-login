from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistroForm, RecuperarPasswordForm

# Usamos un diccionario simple para contar los intentos fallidos.
# Nota: Esto se reinicia cada vez que el servidor se reinicia.
intentos_fallidos = {}

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    # CORRECCIÓN: Añadida la ruta completa de la plantilla
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    # Usamos request.POST.get para evitar errores si la clave no existe
    username = request.POST.get('username', None)

    if request.method == 'POST':
        # Verificación de bloqueo
        if username and username in intentos_fallidos and intentos_fallidos[username] >= 3:
            messages.error(request, 'Clave bloqueada. Demasiados intentos fallidos.')
            # CORRECCIÓN: Redirigimos para evitar reenvío de formulario
            return redirect('login')

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Si el login es exitoso, reiniciamos el contador de intentos
            if username in intentos_fallidos:
                del intentos_fallidos[username]
                
            return redirect('bienvenida')
        else:
            # Si el login falla, incrementamos el contador
            if username:
                intentos_fallidos[username] = intentos_fallidos.get(username, 0) + 1
            
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            
            # --- CORRECCIÓN CLAVE (Patrón PRG) ---
            # En lugar de renderizar, redirigimos para evitar que se reenvíe el formulario al actualizar.
            return redirect('login')
    else:
        form = AuthenticationForm()

    # CORRECCIÓN: Añadida la ruta completa de la plantilla
    return render(request, 'login.html', {'form': form})


def bienvenida_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # CORRECCIÓN: Añadida la ruta completa de la plantilla
    return render(request, 'bienvenida.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


# --- NUEVAS VISTAS PARA RECUPERACIÓN DE CONTRASEÑA ---
def recuperar_password_view(request):
    """Vista para mostrar el formulario de recuperación de contraseña"""
    if request.method == 'POST':
        form = RecuperarPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Aquí simularemos el envío del correo
            messages.success(request, f'La clave de recuperación fue enviada a {email}')
            return redirect('recuperar_confirmacion')
    else:
        form = RecuperarPasswordForm()
    
    return render(request, 'recuperar_password.html', {'form': form})


def recuperar_confirmacion_view(request):
    """Vista para mostrar la confirmación del envío ficticio del correo"""
    return render(request, 'recuperar_confirmacion.html')


