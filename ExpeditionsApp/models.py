from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Expedition(models.Model):
    reference = models.CharField(unique=True, editable=False, max_length=20)
    poids_kg = models.DecimalField(decimal_places=3, max_digits=10)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('publiee', 'Publiee'),
            ('attribuee', 'Attribuee'),
            ('en_cours', 'En_cours'),
            ('livree', 'Livree'),
            ('annulee', 'Annulee'),
        ],
        default='publiee',
    )
    date_souhaitee = models.DateField()
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(
        'EntreprisesApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='expeditions',
    )

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()
        return super().save(*args, **kwargs)

    @classmethod
    def _generate_ref(cls):
        # %Y donne 2026, %y donne 26.
        annee = timezone.now().strftime('%y')
        prefixe = f'EXP-{annee}-'
        # Tri descendant : la plus grande reference de l'annee est en premier.
        last_elem = cls.objects.filter(reference__startswith=prefixe).order_by('-reference').first()
        compteur = int(last_elem.reference[-5:]) + 1 if last_elem else 1
        if compteur > 99999:
            raise ValidationError("le nombre d'expeditions depasse 99999")
        return f'{prefixe}{compteur:05d}'

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError('une expedition ne peut etre publiee que par une entreprise chargeur')
