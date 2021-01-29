from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from Cart.models import Cart
from products.models import Product


# Create your views here.
class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_create(self.request)

        context['object-list'] = self.get_queryset()

        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.get_search(query)
        return Product.objects.none()
