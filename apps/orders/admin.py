from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        "product_id",
        "product_name",
        "price",
        "quantity",
        "size",
        "color",
        "image",
    )
    readonly_fields = ()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_customer_name",
        "email",
        "phone",
        "city",
        "country",
        "total",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "country",
    )

    list_filter = (
        "country",
        "city",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    inlines = [OrderItemInline]

    fieldsets = (
        ("Customer Information", {
            "fields": (
                "user",
                "first_name",
                "last_name",
                "email",
                "phone",
            )
        }),
        ("Delivery Address", {
            "fields": (
                "address",
                "city",
                "country",
                "postal_code",
            )
        }),
        ("Payment Summary", {
            "fields": (
                "subtotal",
                "delivery",
                "total",
            )
        }),
        ("Order Date", {
            "fields": ("created_at",)
        }),
    )

    @admin.display(description="Customer Name")
    def get_customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
