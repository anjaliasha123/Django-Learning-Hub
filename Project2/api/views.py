from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Max
from rest_framework.views import Response
from rest_framework.decorators import api_view
from api.serializers import OrderSerializer, ProductSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    # return JsonResponse({
    #     'data': serializer.data
    # })
    return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT'])
def product_detail(request, pk):
    # product = Product.objects.get(pk=pk)
    product = get_object_or_404(klass=Product,pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects\
        .prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count' : len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)