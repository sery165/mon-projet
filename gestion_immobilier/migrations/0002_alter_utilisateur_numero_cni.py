# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immobilier', '0001_initial'),  # Assurez-vous que la dépendance pointe vers la dernière migration valide
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='numero_cni',
            field=models.CharField(default='0000000000', max_length=15),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='contact',
            field=models.CharField(max_length=15, default=''),
        ),
    ]
