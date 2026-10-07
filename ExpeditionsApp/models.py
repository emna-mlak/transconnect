from django.db import models
from EntrepriseApp.models import Entreprise
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Expedition(models.Model):
    reference = models.CharField(max_length=11, unique = True)
    ville_depart=models.CharField(max_length=15)
    ville_arrivee=models.CharField(max_length=15)
    poids_kg= models.DecimalField(max_digits=3, decimal_places=2)
    date_souhaitee=models.DateField(default=timezone.localdate)
    description = models.TextField(blank=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('publiee', 'Publiée'),
            ('attribuee', 'Attribuée'),
            ('en_cours', 'En cours'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='publiee',
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='expeditions',    null=True,blank=True,)

    def clean(self):
        super().clean()
        #regles metier
        #self.entreprise_id echerche d id meme que avec .
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise':"Une expedition ne peut pas etre crée que par une entreprise de type chargeur"})

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP_(annee)_"
        dernier=cls.objects.filter(reference__startwith=prefixe).order_by('reference').last()
        compteur=(int(dernier.reference[-5:])+1 if dernier else 1)
        if compteur> 99999:
            raise ValidationError('Limit exceeded')
        return f'{prefixe}{compteur:05d}'

    def save(self,*args, **kwargs):
        if not self.reference:
            self.reference=self._generate_ref()
        self.full_clean()
        super().save(*args,**kwargs)