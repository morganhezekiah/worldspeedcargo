
from django.contrib import admin
from django.urls import path

from pages.views import index, track, trackPDF

urlpatterns = [
    path('', index, name="homePage"),
    path('track', track, name="track"),
    path("trackPDF", trackPDF, name="trackPDF"),
    path('admin/', admin.site.urls),
]
