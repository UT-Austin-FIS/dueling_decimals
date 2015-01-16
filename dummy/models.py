from django.db import models


class Dummy(models.Model):
    a = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )

    b = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
    )
