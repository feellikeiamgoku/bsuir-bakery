
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authenication.urls', namespace='authentication')),
    path("api/", include("products.urls", namespace="products")),
    path("site/", include("product_views.urls", namespace="product_views"))
]

urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)