from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product
from Cart.models import Cart


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


# this is a function based view that renders view according to template
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/product_list.html", context)


class ProductFeatureListView(ListView):
    queryset = Product.objects.get_in_stock()
    template_name = "products/product_list.html"


class ProductFeatureDetailView(DetailView):
    queryset = Product.objects.get_in_stock()
    template_name = "products/product_detail_featured.html"


# this function uses the DetailView Template to return detail view of object
class ProductSlugDetailView(DetailView):
    template_name = "products/product_detail.html"
    queryset = Product.objects.all()

    # function get context data to get the data of context of query set found in class based view
    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_create(self.request)
        context['cart'] = cart_obj
        return context

    # takes in request from URL including parameters through **kwargs
    # taking in these parameters it queries for a specific object and then returns an instance
    def get_object(self, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()

        return instance

# use of pk which stands as primary key for argument. produces detail view of object. can take other args and keyword
# args get_object_or_404 returns object or sends a 404 error that shows object does not exist
# def product_detail_view(request, pk=None, *args, **kwargs): #  uses a defined function in the # objects manager
# model that filters using id's. A manager model class created in model class to manipulate queries instance =
# Product.objects.get_by_id(pk)
#
#     if instance is None:
#         raise Http404("Product does not exist")
#     # qs = Product.objects.filter(id=pk)
#     # if qs.count() == 1:
#     #     instance = qs.first()
#     # else:
#     #     raise Http404("Product does not exist")
#     context = {
#         'object': instance
#     }
#     return render(request, "products/product_detail.html", context)
