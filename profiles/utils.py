import pytz
import logging

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms

from profiles.models import Profile

logger = logging.getLogger('app_logger')


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


class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["profile_picture"]
        labels = {
            'profile_picture': "Imagen de Perfil"
        }


def academia_blockchain_timezones():
    tz_list = []
    for tz in pytz.all_timezones:
        if tz.startswith("America"):
            tz_list.append(tz)
        elif tz.startswith("Europe"):
            tz_list.append(tz)
    return tz_list


def get_cryptos_string(profile):
    c_list = profile.cryptos_list()
    logger.info("c_list: %s" % c_list)
    cryptos_string = ""
    for c in c_list:
        cryptos_string += (c.crypto.code + ", ")  # arma string para el frontend
    if len(cryptos_string) > 2:
        cryptos_string = cryptos_string[:-2]

    return cryptos_string
