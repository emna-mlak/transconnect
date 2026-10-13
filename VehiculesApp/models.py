from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    capacite_kg = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'une capacite nulle est invalide'),
            MaxValueValidator(1000, 'une capacite sup a 1000kg est invalide'),
        ],
    )
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_vehicule = models.CharField(
        max_length=20,
        choices=[
            ('camionnette', 'Camionnette'),
            ('fourgon', 'Fourgon'),
            ('camion_porteur', 'Camion_porteur'),
            ('semi_remorque', 'Semi_remorque'),
        ],
    )
    entreprise = models.ForeignKey(
        'EntreprisesApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules',
    )

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError('un vehicule ne peut etre associe a une entreprise non transporteur')
