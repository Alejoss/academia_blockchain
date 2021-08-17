import pytz
import logging
import requests

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms
from django.conf import settings
from django.template import loader

from profiles.models import Profile
from courses.models import Certificate


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
    Cambia el send_mail por con la config de mailgun
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

        logger.warning("EMAIL SENT")

        send_email_message(
            receiver_email=to_email,
            subject="CAMBIA TU CONTRASEÑA - Academia Blockchain",
            message=body
        )


class AcademiaSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Repite la Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
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


def send_confirmation_email(request, user, user_email):
    # Enviar email de confirmacion
    activation_token = PasswordResetTokenGenerator().make_token(user)
    logger.info("activation_token: %s" % activation_token)
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    logger.info("uid: %s" % uid)

    message = render_to_string('profiles/email_confirm_account.html', {
        'username': user.username,
        'uid': uid,
        'token': activation_token,
        'domain': current_site
    })
    send_email_message(subject="Activa tu cuenta",
                       message=message,
                       receiver_email=user_email
                       )

    logger.debug("current_site: %s" % current_site)
    logger.debug("uid: %s" % uid)
    logger.debug("activation_token: %s" % activation_token)


def get_user_diamonds(user, certificates=None):
    if not certificates:
        certificates = Certificate.objects.filter(user=user, deleted=False)

    green_diamonds = certificates.filter(event__event_type="EVENT").count()
    yellow_diamonds = certificates.filter(event__event_type="LIVE_COURSE").count()
    magenta_diamonds = certificates.filter(event__event_type="PRE_RECORDED").count()
    blue_diamonds = certificates.filter(event__event_type="EXAM").count()

    logger.info("certificates: %s" % certificates)
    logger.info("green_diamonds: %s" % green_diamonds)
    logger.info("yellow_diamonds: %s" % yellow_diamonds)
    logger.info("magenta_diamonds: %s" % magenta_diamonds)
    logger.info("blue_diamonds: %s" % blue_diamonds)

    return {"green_diamonds": green_diamonds, "yellow_diamonds": yellow_diamonds, "magenta_diamonds": magenta_diamonds,
            "blue_diamonds": blue_diamonds}
