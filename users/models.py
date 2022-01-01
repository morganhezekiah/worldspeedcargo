
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self,email, password):
        if not email:
            raise ValueError("Please enter an email")

        if not password:
            raise ValueError("Please enter a password")

        
        email = self.normalize_email(email)
        user = self.model(email=email,password=make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email, password)
        user.is_active=True
        user.is_super=True
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    is_super = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD="email"
    PASSWORD_FIELD="password"
    REQUIRED_FIELDS = ['password']


    def has_perm(self, obj):
        return True

    def has_module_perms(self, obj):
        return True

    def equals(self,  object):
        return self.id == object.id
    
    object = UserManager()





class Shipment(models.Model):
    shipper_name = models.TextField()
    shipper_phone = models.TextField()
    shipper_address = models.TextField()
    shipper_email = models.TextField()

    reciever_name = models.TextField()
    reciever_phone = models.TextField()
    reciever_address = models.TextField()
    reciever_email = models.TextField()

    type_of_shipment = models.TextField()
    weight = models.TextField()
    courier = models.TextField()
    packages = models.TextField()
    mode = models.TextField()
    product = models.TextField()
    quantity = models.TextField()
    payment_mode = models.TextField()
    total_freight = models.TextField()
    carrier = models.TextField()
    carrier_reference_no = models.TextField()
    depature_time = models.TextField()
    origin = models.TextField()
    destination = models.TextField()
    pickup_date = models.TextField()
    pickup_time = models.TextField()
    exected_delivery_date = models.TextField()
    comment = models.TextField()
    create_on = models.DateField(default=timezone.now)
    location = models.TextField(default="England")

    uuid = models.CharField(max_length=100, unique=True)
  
    

    def __str__(self) -> str:
        return self.uuid



# class Location(models.Model):
#     date = models.DateField(default=timezone.now)
#     location = models.TextField()
#     status = models.TextField()
#     updated_by = models.TextField()
#     remarks = models.TextField()
#     shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)


#     def __str__(self) -> str:
#         return self.shipment