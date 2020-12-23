from django.contrib import admin

from .models import Influencer


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ["username", "platform", "picture"]
