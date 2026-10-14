from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Entreprise, Utilisateur


@admin.register(Utilisateur) #Ou bien admin.site.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_staff', 'is_active') # ce qui est affiché dans la liste des utilisateurs
    list_filter = ('role', 'is_staff', 'is_active') #ken valeur barka liste_filter=('role',)#ken nheb wehed barka
    list_editable=('role','is_staff') #ken nheb fi tabb les valeurs nbadelhom
    search_fields = ('user_id', 'username', 'email') #fi bar de re recherche nbadel es critere de recherche 

    ordering = ('user_id',)

   

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal')
