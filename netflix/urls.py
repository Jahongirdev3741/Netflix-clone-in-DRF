from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('_admin/', admin.site.urls),
    path('movie/',include('movie.urls')),
]
