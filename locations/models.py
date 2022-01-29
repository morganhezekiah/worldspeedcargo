from django.utils import timezone

from users.models import Shipment
from django.db import models




class Location(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.DateTimeField(default=timezone.now)
    location = models.TextField()
    status = models.TextField()
    remark = models.TextField(null=True, blank=True)
    shipment = models.ForeignKey(Shipment,related_name="locate", on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.shipment.uuid

    def returnStatusLabelType(self):
        main ="label"
        if self.status == "Delivered":
            main = f"{main} label-success"
        elif self.status == "Cancelled":
            main = f"{main} label-danger"
        elif self.status == "On Hold":
            main = f"{main} label-warning"
        elif self.status == "In Transit":
            main = f"{main} label-primary"
        else:
            main = f"{main} label-default"

        return main