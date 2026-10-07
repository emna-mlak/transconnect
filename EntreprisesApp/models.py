from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


matricule_fiscal_validator = RegexValidator(regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$', message ="Format incorrect")

def validate_email(value):
    if not value:
        raise ValidationError("L'addresse email est obligatoire")
    if not value.endswith('@gmail.com'):
        raise ValidationError("Format invalide")

# from django.cor impot validators 
# Create your models here.
class Utilisateur(AbstractUser):
    user_id=models.CharField(max_length=8, primary_key=True)
    email = models.EmailField(unique = True, validators=[validate_email])#pour evite blocage dans l ahout eviter()
    role = models.CharField(max_length=20, choices=[
        ('admin','Admin'),
        ('chargeur','Chargeur'),
        ('transporteur','Transporteur')
    ], default = 'chargeur'
    )
    telephone = models.CharField(max_length=15, null = False, blank= False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, null = False, blank= False)
    matricule_fiscale = models.CharField(max_length=17, unique = True, validators=[matricule_fiscal_validator])
    type_entreprise = models.CharField(max_length=100, choices=[
        ('chargeur','Chargeur'),
        ('transporteur','Transporteur')
    ], default = 'chargeur')

    adresse = models.TextField(validators=[MinLengthValidator(10, "Adresse doit etre sup à 10"),MaxLengthValidator(300, "Adresse doit etre min à 300")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    gerant=models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')
    @classmethod
    def _generate_user(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"annee[-2:]"
        dernier=cls.objects.filter(reference__startwith=prefixe).order_by('reference').last()
        compteur=(int(dernier.reference[-5:])+1 if dernier else 1)
        if compteur> 99999:
            raise ValidationError('Limit exceeded')
        return f'{prefixe}{compteur:05d}'

    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime('%y')       
        prefixe = f"{annee}user"                       
        dernier = cls.objects.filter(user_id__startswith=prefixe).order_by('user_id').last()
        compteur = int(dernier.user_id[-2:]) + 1 if dernier else 0
        if compteur > 99:
            raise ValidationError('Limite de 100 inscriptions atteinte pour cette année')
        return f'{prefixe}{compteur:02d}'             

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        self.full_clean()
        super().save(*args, **kwargs)