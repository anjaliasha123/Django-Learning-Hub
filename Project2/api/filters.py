import django_filters
from api.models import Product
# Query Parameters
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price' : ['lt', 'gt', 'exact', 'range'],
            'name' : ['iexact', 'icontains'],
        }