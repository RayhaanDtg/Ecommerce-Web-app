from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from ecom.serializers import ProductSerializer,CartSerializer,OrderSerializer,StockSerializer
from .models import Product
from Cart.models import Cart
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from stock.models import Stock


# class based view that renders view without template. needs function get context data to render objects of a query set
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    # # function get context data to get the data of context of query set found in class based view
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_create(self.request)
        context['cart'] = cart_obj
        return context


# this is a function based view that renders view according to template. Returns a list of the products and there stock
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list_view(request):
    print("here is request data for products")
    product_list_stock=[]
    queryset = Product.objects.all()
    for p in queryset:
        qs_stock=Stock.objects.filter(product=p,active=True)
        stock=qs_stock.first()
        print(stock)
        stock_serialized= StockSerializer(stock)
        product_serialized=ProductSerializer(p)
        product_list_stock.append({
            'stock':stock_serialized.data,
            'product':product_serialized.data
        })

    json_data = {
        'products': product_list_stock
        
    }
    return JsonResponse(json_data)


# Gets the details of the product, using the slug.Also gets the most active stock pertaining to the product
# serializers the stock and the product and returns them as json data
@api_view(['GET'])
@permission_classes([AllowAny])
def product_slug_view(request,slug):
    stock=None
    try:
        instance = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    except Product.MultipleObjectsReturned:
        qs=Product.objects.filter(slug=slug)
        instance=qs.first()
    try:
        qs_stock=Stock.objects.get_queryset().filter(product=instance,active=True)
        stock=qs_stock.first()
    except Stock.DoesNotExist:
        raise Http404("Stock does not exist")
   
    
    stock_serializer=StockSerializer(stock)
    product_serializer=ProductSerializer(instance)
    
    
    json_data={
        'stock':stock_serializer.data,
        'product':product_serializer.data
    }
    return JsonResponse(json_data,safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])  
def product_id_details(request,id):
    stock=None
    try:
        instance=Product.objects.get_by_id(id=id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    except Product.MultipleObjectsReturned:
        qs=Product.objects.filter(slug=slug)
        instance=qs.first()

    try:
        qs_stock=Stock.objects.get_queryset().filter(product=instance,active=True)
        stock=qs_stock.first()
    except Stock.DoesNotExist:
        raise Http404("Stock does not exist")
    
    stock_serializer=StockSerializer(stock)
    product_serializer=ProductSerializer(instance)
    
    
    json_data={
        'stock':stock_serializer.data,
        'product':product_serializer.data
    }
    return JsonResponse(json_data,safe=False)

            
       
          

       


# class ProductFeatureListView(ListView):
#     queryset = Product.objects.get_in_stock()
#     template_name = "products/product_list.html"


# class ProductFeatureDetailView(DetailView):
#     queryset = Product.objects.get_in_stock()
#     template_name = "products/product_detail_featured.html"


# # this function uses the DetailView Template to return detail view of object
# class ProductSlugDetailView(DetailView):
#     template_name = "products/product_detail.html"
#     queryset = Product.objects.all()

#     # function get context data to get the data of context of query set found in class based view
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_create(self.request)
#         context['cart'] = cart_obj
#         return context

#     # takes in request from URL including parameters through **kwargs
#     # taking in these parameters it queries for a specific object and then returns an instance
#     def get_object(self, *args, **kwargs):
#         slug = self.kwargs['slug']
#         try:
#             instance = Product.objects.get(slug=slug)
#         except Product.DoesNotExist:
#             raise Http404("Product does not exist")

#         except Product.MultipleObjectsReturned:
#             qs = Product.objects.filter(slug=slug)
#             instance = qs.first()

#         return instance

