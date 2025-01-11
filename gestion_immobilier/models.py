from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Modèle pour les communes
class Commune(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

# Modèle pour les types de chambres
class TypeChambre(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom

# Modèle pour gérer les images de la chambre
class ImageChambre(models.Model):
    chambre = models.ForeignKey('Chambre', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chambres/%Y/%m/%d/')
    
    def __str__(self):
        return f"Image pour {self.chambre}"

# Modèle pour les chambres
class Chambre(models.Model):
    type_chambre = models.ForeignKey(TypeChambre, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    description = models.TextField()
    prix = models.CharField(max_length=15)
    superficie = models.FloatField(help_text="Superficie en m²")
    nombre_de_chambres = models.IntegerField()
    nombre_de_salons = models.IntegerField()
    adresse = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, null=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Nouveaux champs
    contact = models.CharField(max_length=15, default='0000000000')
    situation_geographique = models.CharField(max_length=255, default='Non spécifiée')

    def __str__(self):
        return f"{self.type_chambre.nom} à {self.commune.nom} ({self.nombre_de_chambres} chambres, {self.nombre_de_salons} salons)"

# Modèle Utilisateur personnalisé
class Utilisateur(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    numero_cni = models.CharField(max_length=15, default='0000000000')  # Utilisation de PositiveIntegerField pour les entiers
    photo_cni = models.ImageField(upload_to='photos_cni/')  # Ajout d'un champ pour la photo de la CNI
    photo = models.ImageField(upload_to='photos_utilisateurs/')  # Changer en PositiveIntegerField pour les entiers
    contact = models.CharField(max_length=15)

    groups = models.ManyToManyField( 
        'auth.Group',
        related_name='utilisateurs',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups', 
    )

    user_permissions = models.ManyToManyField( 
        'auth.Permission',
        related_name='utilisateurs_permissions',
        blank=True, 
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
     )

    def __str__(self):
        return f' {self.username} {self.nom} {self.prenom}'
