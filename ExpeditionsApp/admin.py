from django.contrib import admin

from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'statut', 'ville_depart', 'ville_arrivee', 'poids_kg', 'entreprise')
    list_filter = ('statut',)
    search_fields = ('reference', 'ville_depart', 'ville_arrivee')
    list_editable = ('statut',)
    ordering = ('-created_at',)
