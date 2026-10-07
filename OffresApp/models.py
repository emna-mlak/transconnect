from django.db import models
from EntrepriseApp.models import Entreprise
from ExpeditionApp.models import Expedition
from VehiculeApp.models import Vehicule
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator



class Offre(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0, "prix doit etre sup à 0")])

    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1, "delai jours doit etre sup à 1")])
    statut = models.CharField(
        max_length=20,
        choices=[
            ('proposee', 'Proposée'),
            ('acceptee', 'Acceptée'),
            ('refusee', 'Refusée'),
            ('retiree', 'Retirée'),
        ],
        default='proposee',
    )
    date_proposition = models.DateField(auto_now_add=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='offres')
    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres'
    )
    vehicule = models.ForeignKey(Vehicule, on_delete=models.PROTECT, related_name='offres')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.transporteur and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError({'transporteur':"Offre relative à in chargeur"})
#vehicule proposé doit apprtenir au meme transporteur
        if self.vehicule_id and self.transporteur_id and  self.vehicule.entreprise_id!= self.transporteur_id:
            raise ValidationError({'vehicule':"Vehicule doit appartenir au meme transporteur"})
        
