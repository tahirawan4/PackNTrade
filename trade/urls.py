from django.urls import path
from django.conf.urls.static import static

from PackageNTrade import settings
from trade.views import home, IndexView

urlpatterns = [
    path('home/', IndexView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
