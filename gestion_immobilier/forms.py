from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Chambre, Utilisateur, ImageChambre

# Formulaire pour la chambre
class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = ['type_chambre', 'commune', 'description', 'prix', 'superficie', 
                  'nombre_de_chambres', 'nombre_de_salons', 'adresse', 'video', 
                  'contact', 'situation_geographique']
        widgets = {
            'video': forms.ClearableFileInput(),
        }

# Formulaire personnalisé pour l'utilisateur
class UserCreationFormCustom(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ('username', 'password1', 'password2', 
                                                 'nom', 'prenom', 'date_naissance', 
                                                 'numero_cni', 'photo_cni', 'photo', 'contact')
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

# Formulaire pour l'image de la chambre
class ImageChambreForm(forms.ModelForm):
    class Meta:
        model = ImageChambre
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(),
        }
