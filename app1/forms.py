from django import forms
from django.contrib.auth.models import User
import re

class RegistroForm(forms.ModelForm):
    # --- Definimos cada campo manualmente para tener control total ---

    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=100,
        help_text="Requerido 100 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.",
        error_messages={
            'required': 'Este campo es obligatorio.',
            'unique': 'Este nombre de usuario ya existe.',
        }
    )
    
    email = forms.EmailField(
        label="Correo Electrónico",
        error_messages={
            'required': 'Este campo es obligatorio.',
            'unique': 'Este correo electrónico ya está en uso.',
            'invalid': 'Por favor, introduce una dirección de correo válida.',
        }
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="Debe tener al menos 8 caracteres, una mayúscula y un número."
    )

    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        # Ahora solo definimos el modelo, los campos ya están definidos arriba
        fields = ['username', 'email', 'password']

    # --- Las validaciones personalizadas se mantienen igual ---

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        
        if password:
            if len(password) < 8:
                self.add_error('password', "La contraseña debe tener al menos 8 caracteres.")
            if not re.search(r'[A-Z]', password):
                self.add_error('password', "La contraseña debe contener al menos una letra mayúscula.")
            if not re.search(r'[0-9]', password):
                self.add_error('password', "La contraseña debe contener al menos un número.")
        
        return cleaned_data


# --- NUEVO FORMULARIO PARA RECUPERACIÓN DE CONTRASEÑA ---
class RecuperarPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa tu correo electrónico',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Por favor, introduce una dirección de correo válida.',
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("No existe una cuenta asociada a este correo electrónico.")
        return email


