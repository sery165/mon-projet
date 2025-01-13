from django.contrib import admin
from .models import Commune, TypeChambre, Chambre, ImageChambre, Utilisateur

# Enregistrement des modèles pour l'admin
admin.site.register(Commune)
admin.site.register(TypeChambre)

# Configuration de l'admin pour Utilisateur
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')  # Ajoutez ici les champs que vous souhaitez afficher
    search_fields = ('username', 'email')

# Vérifier si le modèle est déjà enregistré
try:
    admin.site.register(Utilisateur, UtilisateurAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Inline admin pour les images de chambre
class ImageChambreInline(admin.TabularInline):
    model = ImageChambre
    extra = 1  # Nombre d'images vides à afficher dans le formulaire

class ChambreAdmin(admin.ModelAdmin):
    inlines = [ImageChambreInline]

# Enregistrement des modèles Chambre et ImageChambre dans l'admin
admin.site.register(Chambre, ChambreAdmin)
admin.site.register(ImageChambre)
