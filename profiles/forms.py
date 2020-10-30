from django import forms
from profiles.models import Profile


class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["profile_picture"]
        labels = {
            'profile_picture': "Imagen de Perfil"
        }
