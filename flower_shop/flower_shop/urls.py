from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    # path('', include(('main.urls', 'main'), namespace='main')), # вариант  с имененным пространством
    # path('catalog/', include('catalog.urls'))
    path('catalog/', include(('catalog.urls', 'catalog'), namespace='catalog')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
