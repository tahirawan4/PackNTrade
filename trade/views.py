from django.shortcuts import render_to_response, render
from django.views import generic, View
from django.views.generic import TemplateView
from trade.models import Product, Category


class IndexView(generic.ListView):
    model = Product, Category
    template_name = 'home.html'
    context_object_name = 'product'

    # def get_queryset(self):
    #     return Product.objects.all(), Category.objects.all()

    def get(self, request, *args, **kwargs):
        # products = Product.objects.all().order_by('-created_at')
        # category = Category.objects.all()
        a = {"products": Product.objects.all().order_by('-created_at'),
             "category": Category.objects.all(), }
        # a = {'products': products}, {'category': category}

        return render(request, self.template_name, a)


class DetailView(TemplateView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        pslug = kwargs.get('pslug')
        product = Product.objects.get(slug=pslug)  # .order_by('created_at')
        products = Product.objects.all()
        return render(request, self.template_name, {'product': product, 'products':products})


class CategoryView(TemplateView):
    model = Category, Product
    template_name = 'detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        cid = kwargs.get('cid')
        category = Category.objects.get(id=cid)  # .order_by('created_at')
        product = Product.objects.filter(category=cid)
        a = {"product_category": product,
             "category": category,
             # and so on for all the desired models...
             }
        return render(request, self.template_name, a)


class CategoryProductView(TemplateView):
    model = Category
    template_name = 'detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        cid = kwargs.get('cid')
        category = Category.objects.get(id=cid)  # .order_by('created_at')
        return render(request, self.template_name, {'category': category})


class CartView(generic.TemplateView):
    model = Product
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('created_at')

        return render(request, self.template_name, {'products': products})
    # render_to_response(template_name)
