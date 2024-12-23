import django_filters

from store.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'title': ['iexact', 'icontains'],
            'collection_id':['exact'],
            'unit_price': ['range', 'exact','lt','gt']
        }