# mon_projet/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importer la vue de connexion

urlpatterns = [
    path('admin/', admin.site.urls),  # Interface d'administration
    path('', include('gestion_immobilier.urls')),  # Inclure les URLs de l'application 'gestion_immobilier'
    # Si vous avez besoin de gérer la connexion avec une page dédiée
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
