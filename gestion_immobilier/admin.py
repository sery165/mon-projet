from django.contrib import admin
from .models import Commune, TypeChambre, Chambre, Utilisateur

# Enregistrement des modèles
admin.site.register(Commune)
admin.site.register(TypeChambre)
admin.site.register(Chambre)

# Configuration de l'admin pour Utilisateur
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')  # Ajoutez ici les champs que vous souhaitez afficher
    search_fields = ('username', 'email')

# Vérifier si le modèle est déjà enregistré
try:
    admin.site.register(Utilisateur, UtilisateurAdmin)
except admin.sites.AlreadyRegistered:
    pass
