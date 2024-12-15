from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.http import HttpResponse
from store.models  import Product, Order, Customer

# Create your views here.

def hello(request):
    # lazy evaluation
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # result = Product.objects.aggregate(count=Count('id'))
    # result = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # print(result)
    # result2 = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    # print(result2)
    # now its activated
    # result = Customer.objects.annotate(orders_count=Count('order'))
    # print(result)

    # content_type = ContentType.objects.get_for_model(Product)
    # result = TaggedItem.objects\
    # .select_related('tag')\
    # .filter(object_id=1, content_type=content_type)
    result = TaggedItem.objects.get_tags_for(Product, 1);
        
    print(result)
    return render(request, 'hello.html', {'name': 'Anna'})