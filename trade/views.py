from django.shortcuts import render_to_response
from django.views import generic

from trade.models import Product


def home(request):
    return render_to_response('home.html', {})


class IndexView(generic.ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.all()
