# Generated by Django 5.1.3 on 2025-01-11 00:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immobilier', '0003_alter_chambre_prix_alter_utilisateur_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chambre',
            name='image',
        ),
        migrations.CreateModel(
            name='ImageChambre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='chambres/%Y/%m/%d/')),
                ('chambre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gestion_immobilier.chambre')),
            ],
        ),
    ]
