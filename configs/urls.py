from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('', include('splash.urls', namespace='splash')),
    path('', include('authentication.urls', namespace='authentication')),
    path('dashboard', include('core.urls', namespace='core')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
