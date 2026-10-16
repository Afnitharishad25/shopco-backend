from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "dress_style",
        "price",
        "rating",
    )

    list_filter = (
        "category",
        "dress_style",
    )

    search_fields = (
        "name",
        "category",
        "dress_style",
    )