from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            queryset.filter(inventory__lt=10)



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    # inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer_name', 'customer_order_count']
    ordering = ['-id']
    list_per_page = 10
    list_select_related = ['customer']

    @admin.display(ordering='customer')
    def customer_name(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'

    @admin.display(ordering='customer_order_count')
    def customer_order_count(self, order):
        url = (
                reverse('admin:store_customer_changelist')
                + '?'
                + urlencode({
            'order__id': str(order.id)
        }))
        return format_html('<a href="{}">{}</a>', url, order.customer_order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_order_count=Count('customer')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )