
from django.contrib import admin
from django.urls import path

from pages.views import index, track, trackPDF,download_shipment_invoice, sitemap
from users.views import deleteShipment, loginUser, create_shipment, shipment_detail, ShipmentListView,create_shipment_location, deleteShipment

urlpatterns = [
    path('', index, name="homePage"),
    path('track', track, name="track"),
    path("sitemap", sitemap, name="sitemap"),
    path("trackPDF", trackPDF, name="trackPDF"),
    path("download_shipment_invoice",download_shipment_invoice, name="download_shipment_invoice"),
    path("users/login", loginUser, name="loginUser"),
    path("users/create-shipment", create_shipment, name="createShipment"),
    path("users/list-shipment", ShipmentListView.as_view(), name="shipment-list"),
    path("users/create-shipment-location", create_shipment_location, name="create_shipment_location"),
    path("users/shipment-detail/<int:pk>", shipment_detail, name="shipment_detail"),
    path("users/delete_shipment/<int:pk>", deleteShipment, name="deleteShipment"),
    path('admin/', admin.site.urls),
]
