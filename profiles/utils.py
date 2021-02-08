import pytz
import logging
import requests

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.template import loader

from profiles.models import Profile


logger = logging.getLogger('app_logger')


def send_email_message(receiver_email, subject, message):
    domain_name = settings.MAILGUN_DOMAIN

    return requests.post(
        "https://api.mailgun.net/v3/" + domain_name + "/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "academiablockchain@no-reply.com",
              "to": [receiver_email],
              "subject": subject,
              "text": message})


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


class AcademiaPasswordResetForm(PasswordResetForm):
    """
    Cambia el send_mail por utiliza send_email_message con la config de mailgun
    """

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """

        # subject = loader.render_to_string(subject_template_name, context)
        # # Email subject *must not* contain newlines
        # subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        #
        # email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # if html_email_template_name is not None:
        #     html_email = loader.render_to_string(html_email_template_name, context)
        #     email_message.attach_alternative(html_email, 'text/html')
        #
        # #

        send_email_message(
            receiver_email=to_email,
            subject="CAMBIA TU CONTRASEÑA - Academia Blockchain",
            message=body

        )


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
