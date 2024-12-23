from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from store.pagination import DefaultPagination
from .models import CartItem, Product, Collection, OrderItem, Review, Cart
from .serializers import AddCartItemSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, UpdateCartItemSerializer
from store.filters import ProductFilter
# Create your views here.

# http://127.0.0.1:8000/store/products/?title__icontains=bread
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description', 'slug']
    ordering_fields = ['title', 'inventory', 'unit_price']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']) > 0:
            return Response({'error': 'product has associated order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    def destroy(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'there are some products associated with this collection'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        collection.delete()
        return Response('succesfully deleted', status=status.HTTP_200_OK)


class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method in ['PATCH']:
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')
