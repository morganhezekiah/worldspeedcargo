import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from users.models import Shipment, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .shipmentSerializer import ShipmentSerializer
from django.urls import reverse
from utils.RandomString import GenerateRandomString


def loginUser(request):
    if request.method== "GET":
        
        return render(request, "users/auth/login.html")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email:
            messages.error(request, "Please enter your email")
            return redirect("/users/login")
        if not password:
            messages.error(request, "Please enter your password")
            return redirect("/users/login")
        
        try:
            u = User.object.get(email=email)
        except User.DoesNotExist as e:
            messages.error(request, "Email is incorrect")
            return redirect("/users/login")

        uPassword = u.password
        if check_password(password, uPassword):
            login(request, user = u)
            return HttpResponseRedirect("/users/create-shipment")
        messages.error(request, "Password is incorrect")
        return redirect("/users/login")


@login_required(login_url="/users/login")
def create_shipment(request):
    if request.method == "GET":
        uuid =  GenerateRandomString.randomStringGenerator(10)
        return render(request, "users/auth/create-shipment.html", {"uuid":uuid})
    else:
        data = request.POST
        s = ShipmentSerializer(data=data)
        if s.is_valid():
            s.save()
            pk  =Shipment.objects.last().id
            return redirect(reverse("shipment_detail", kwargs= {"pk":pk}))
        else:
            return redirect(reverse("createShipment"))




@login_required(login_url="/users/login")
def shipment_detail(request, pk):
    if request.method == "GET":
        try:
            s= Shipment.objects.get(id=pk)
        except Shipment.DoesNotExist as e:
            s = {}
        return render(request, "users/auth/shipment-details.html", { "shipment": s})
    else:
        data = request.POST
        instance = Shipment.objects.get(id=pk)
        s = ShipmentSerializer(data=data, instance=instance)
        if s.is_valid():
            s.save()
            messages.success(request, "Shipment editted successfully")
        else:
            messages.error(request, "Shipment editted unsuccessfully")
        return HttpResponseRedirect(f"/users/shipment-detail/{instance.pk}")



@login_required(login_url="/users/login")
def shipment_list(request):
    s = Shipment.objects.all().order_by("-id")
    print(s)
    return render(request,  "users/auth/list_shipment.html", {"shipments":s})


@login_required(login_url="/users/login")
def create_shipment_location(request):
    pass