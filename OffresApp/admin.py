from django.contrib import admin

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'statut', 'prix', 'delai_jours', 'expedition', 'transporteur', 'vehicule')
    list_filter = ('statut',)
    search_fields = ('expedition__reference', 'transporteur__raison_sociale')
    list_editable = ('statut',)
    ordering = ('-created_at',)
