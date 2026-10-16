from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=500)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    discount = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    category = models.CharField(max_length=100)

    colors = models.JSONField(default=list)

    sizes = models.JSONField(default=list)

    dress_style = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name