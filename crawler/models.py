from django.db import models


class PlatformTypes(models.TextChoices):
    INSTAGRAM = "Instagram", "Instagram"


class Influencer(models.Model):
    username = models.CharField(max_length=50)
    platform = models.CharField(
        max_length=50,
        choices=PlatformTypes.choices,
        default=PlatformTypes.INSTAGRAM,
    )
    picture = models.URLField()
