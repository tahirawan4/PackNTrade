from django.urls import path
from django.conf.urls.static import static

from PackageNTrade import settings
from trade.views import IndexView, DetailView, CategoryView, CartView

urlpatterns = [
    path('home/', IndexView.as_view()),
    path('detail/<slug:pslug>/', DetailView.as_view(),name='details'),
    path('category/<int:cid>/', CategoryView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
