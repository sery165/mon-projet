import logging  # Ajoutez cette ligne en haut de votre fichier

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Chambre, Commune, TypeChambre
from .forms import ChambreForm, UserCreationFormCustom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chambre, ImageChambre
from .forms import ChambreForm, ImageChambreForm  # Assurez-vous d'importer ImageChambreForm
import logging  # Vous avez déjà cette ligne maintenant

logger = logging.getLogger(__name__)

# Afficher toutes les chambres selon les critères
def accueil(request):
    chambres = Chambre.objects.all()
    return render(request, 'gestion_immobilier/accueil.html', {'chambres': chambres})

# Voir les chambres d'une commune
def commune_chambres(request, commune_id):
    commune = get_object_or_404(Commune, id=commune_id)
    chambres = Chambre.objects.filter(commune=commune)
    return render(request, 'gestion_immobilier/commune_chambres.html', {'commune': commune, 'chambres': chambres})

# Ajouter une chambre (accessible uniquement aux utilisateurs connectés)
@login_required
def ajouter_chambre(request):
    if request.method == 'POST':
        # Créer les instances des formulaires
        chambre_form = ChambreForm(request.POST, request.FILES)
        image_form = ImageChambreForm(request.POST, request.FILES)

        if chambre_form.is_valid() and image_form.is_valid():
            # Sauver la chambre
            chambre = chambre_form.save(commit=False)
            chambre.utilisateur = request.user  # Utilisateur connecté
            chambre.save()

            # Sauver l'image associée à la chambre
            image = image_form.save(commit=False)
            image.chambre = chambre
            image.save()

            # Redirection après l'ajout
            return redirect('accueil')  # Redirige vers la page d'accueil ou la page des chambres
    else:
        chambre_form = ChambreForm()
        image_form = ImageChambreForm()

    return render(request, 'gestion_immobilier/ajouter_chambre.html', {
        'chambre_form': chambre_form,
        'image_form': image_form,
    })

# Inscription d'un nouvel utilisateur
def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UserCreationFormCustom(request.POST, request.FILES)
        if form.is_valid():
            UserCreation= form.save()
            login(request, UserCreation)
            return redirect('accueil')
    else:
        form = UserCreationFormCustom()
    return render(request, 'gestion_immobilier/ajouter_utilisateur.html', {'form': form})

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('home')  # Redirection vers la page d'accueil
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
            return redirect('login')  # Redirection vers la page de connexion en cas d'erreur
    
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Le mot de passe est haché automatiquement ici
            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        else:
            messages.error(request, 'Erreur dans le formulaire. Veuillez réessayer.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Chambre  # Assurez-vous que vous avez un modèle Chambre avec des images associées
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def generate_chambre_pdf(request, chambre_id):
    # Récupérer la chambre depuis la base de données
    chambre = Chambre.objects.get(id=chambre_id)
    
    # Création d'un fichier PDF en mémoire
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Ajoutez le titre de la chambre dans le PDF
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, f"Chambre #{chambre.id}")
    
    # Si la chambre a des images, vous pouvez les ajouter
    y_position = 720  # Position verticale initiale pour placer les images
    for image in chambre.images.all():  # Assurez-vous que votre modèle a un champ d'images (par exemple un champ ImageField)
        # Chargement de l'image
        image_path = default_storage.path(image.file.name)
        c.drawImage(image_path, 100, y_position, width=400, height=300)
        y_position -= 320  # Déplacer la position pour l'image suivante
        
        if y_position < 50:  # Si on atteint le bas de la page, on crée une nouvelle page
            c.showPage()
            y_position = 750
    
    # Sauvegarder le PDF dans le buffer
    c.showPage()
    c.save()

    # Récupérer le contenu du buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Retourner la réponse HTTP avec le PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="chambre_{chambre_id}.pdf"'
    return response

def profile(request):
    return render(request, 'profile.html')

from django.contrib.auth.models import User

def check_user_status(username):
    try:
        user = User.objects.get(username=username)
        if user.is_active:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False
    
    import logging
logger = logging.getLogger(__name__)

def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            logger.debug("Tentative de connexion avec l'utilisateur: %s", username)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                logger.debug("Authentification réussie pour l'utilisateur: %s", username)
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                return redirect('home')  # Redirection vers la page d'accueil
            else:
                logger.warning("Échec de la connexion pour l'utilisateur: %s", username)
                messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
                return redirect('login')  # Redirection vers la page de connexion en cas d'erreur
        else:
            logger.debug("Méthode de requête non-POST pour la vue de connexion.")
    except Exception as e:
        logger.exception("Erreur lors de la tentative de connexion: %s", str(e))

    return render(request, 'registration/login.html')

from django.contrib.auth import authenticate

def test_authentication():
    username = 'votre_nom_dutilisateur'
    password = 'votre_mot_de_passe'
    user = authenticate(username=username, password=password)
    if user is not None:
        print("Authentification réussie pour l'utilisateur:", username)
    else:
        print("Échec de l'authentification pour l'utilisateur:", username)

from django.shortcuts import render

def contact_view(request):
    return render(request, 'contact.html')
def services_view(request): 
    return render(request, 'services.html')

def index_view(request):
    return render(request, 'index.html')