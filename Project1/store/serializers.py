from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()
    class Meta:
        model = Collection
        fields = ['id', 'title',  'products_count']

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_tax')
#     # collection = serializers.StringRelatedField()
#     # collection = CollectionSerializer()
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name = 'collection-detail',
#     )

class ProductSerializer(serializers.ModelSerializer):
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail',
    # )
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price' , 'inventory', 'collection' ]
        
    def calculate_price_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance