from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # LEARNING URLS
    path("api/", include("apps.learning.urls")),
]
