from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms


class AcademiaUserCreationForm(UserCreationForm):
    # Cambia el idioma del form de django como sea necesario

    class Meta:
        fields = ('username', 'email')
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control border', 'id': 'username', 'name': 'username',
                                                         'placeholder': "Nombre de Usuario"}),
            'email': forms.TextInput(attrs={'class': 'form-control border', 'id': 'email', 'name': 'email',
                                               'placeholder': "Correo Electrónico"})
        }

class AcademiaLoginForm(AuthenticationForm):
    # Cambia el idioma del form de django como sea necesario

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'class': 'form-control border', 'id': 'username',
                                                           'name': 'username',
                                                           'placeholder': "Nombre de Usuario"
                                                           }))
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control border', 'id': 'email', 'name': 'email',
                                          'placeholder': "Contraseña"
                                          }),
    )
