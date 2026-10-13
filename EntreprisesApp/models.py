from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


def validate_email(value):
    if not value:
        raise ValidationError('un email est requis')
    if not value.endswith('@gmail.com'):
        raise ValidationError('un email valide est requis')
    return value


class UtilisateurManager(UserManager):
    def _create_user_object(self, username, email, password, **extra_fields):
        if not extra_fields.get('user_id'):
            extra_fields['user_id'] = self.model._generate_user_id()
        return super()._create_user_object(username, email, password, **extra_fields)


class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, editable=False)
    email = models.EmailField(unique=True, validators=[validate_email])
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
            ('admin', 'Administrateur'),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UtilisateurManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_user_id(cls):
        last = cls.objects.order_by('-user_id').first()
        numero = 1
        if last is not None and str(last.user_id).startswith('USR') and str(last.user_id)[3:].isdigit():
            numero = int(str(last.user_id)[3:]) + 1
        if numero > 99999:
            raise ValidationError("le nombre d'utilisateurs depasse 99999")
        return f'USR{numero:05d}'


# Declare hors de la classe pour le reutiliser ailleurs.
matricule_validators = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
)


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=100)
    matricule_fiscal = models.CharField(max_length=17, unique=True, validators=[matricule_validators])
    type_entreprise = models.CharField(
        max_length=20,
        choices=[('chargeur', 'Chargeur'), ('transporteur', 'Transporteur')],
        default='chargeur',
    )
    adresse = models.TextField(validators=[MinLengthValidator(10, 'une adresse minimale de 10 caracteres est requise')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')
