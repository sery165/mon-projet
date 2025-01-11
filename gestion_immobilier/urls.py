from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # Importer include
from . import views
from .views import contact_view, services_view, index_view

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('commune/<int:commune_id>/', views.commune_chambres, name='commune_chambres'),
    path('ajouter_chambre/', views.ajouter_chambre, name='ajouter_chambre'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclure les URLs d'authentification standard de Django
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chambre/<int:chambre_id>/pdf/', views.generate_chambre_pdf, name='generate_chambre_pdf'),
    path('profile/', views.profile, name='profile'),  # URL pour le profil
    path('contact.html/', contact_view, name='contact'),
    path('services.html', services_view, name='services'),
    path('index.html', index_view, name='index'),  # Ajout de l'URL pour index.html
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
