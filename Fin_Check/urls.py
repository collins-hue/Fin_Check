
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from Fin_Check import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budget_app.urls', namespace='budget_app'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
