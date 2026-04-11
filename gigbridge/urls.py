from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),

    # Uncomment when other members create their urls.py
    # path('accounts/', include('accounts.urls', namespace='accounts')),
    # path('tasks/', include('tasks.urls', namespace='tasks')),
    # path('proposals/', include('proposals.urls', namespace='proposals')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)