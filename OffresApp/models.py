from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Offre(models.Model):
    date_proposition = models.DateField(auto_now_add=True)
    delai_jours = models.PositiveIntegerField()
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, 'un prix nul est invalide')],
    )
    statut = models.CharField(
        max_length=10,
        choices=[
            ('proposee', 'Proposee'),
            ('acceptee', 'Acceptee'),
            ('refusee', 'Refusee'),
            ('retiree', 'Retiree'),
        ],
        default='proposee',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expedition = models.ForeignKey(
        'ExpeditionsApp.Expedition',
        on_delete=models.CASCADE,
        related_name='offres',
    )
    vehicule = models.ForeignKey(
        'VehiculesApp.Vehicule',
        on_delete=models.CASCADE,
        related_name='offres',
    )
    transporteur = models.ForeignKey(
        'EntreprisesApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='offres',
    )

    def clean(self):
        super().clean()
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError('une offre ne peut etre proposee que par une entreprise transporteur')
        if self.vehicule_id and self.transporteur_id and self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError('le vehicule doit appartenir au transporteur')
        if self.vehicule_id and not self.vehicule.disponible:
            raise ValidationError('le vehicule doit etre disponible')
        if self.statut == 'proposee' and self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError('une offre ne peut etre proposee que sur une expedition publiee')
