from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from locations.forms import AddLocationForm
from locations.models import Location
from users.models import Shipment, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .shipmentSerializer import ShipmentSerializer
from django.urls import reverse
from utils.RandomString import GenerateRandomString
from utils.SendEmail import SendEmail
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from threading import Thread

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
        print(data)
        s = ShipmentSerializer(data=data)
        if s.is_valid():
            print("saving")
            s.save()
            pk  =Shipment.objects.last().id
            return redirect(reverse("shipment_detail", kwargs= {"pk":pk}))
        else:
            print(s.errors)
            return redirect(reverse("createShipment"))


def sendShipmentComplaint(request):
    if request.method == "POST":
        message = request.POST.get("message")
        s = SendEmail(message, "Complaint From Worldspeedcargo")
        t = Thread(target = s.send)
        t.start()
        return JsonResponse({"message":"Message Sent "}, status=200)

@login_required(login_url="/users/login")
def shipment_detail(request, pk):
    if request.method == "GET":
        try:
            s= Shipment.objects.get(id=pk)
            l = Location.objects.filter(shipment = s)
            
        except Shipment.DoesNotExist as e:
            s = {}
            l ={}
        addLocationForm= AddLocationForm()
        return render(request, "users/auth/shipment-details.html", { "shipment": s,"addLocationForm":addLocationForm, 'location':l})
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



class ShipmentListView(LoginRequiredMixin,View):
    def get(self, request):
        s = Shipment.objects.all().order_by("-id")
        return render(request,  "users/auth/list_shipment.html", {"shipments":s,"count":len(s)})

def deleteShipment(request, pk):
    try:
        s = Shipment.objects.get(id=pk)
        s.delete()
        return JsonResponse({"success":True}, status=200)
    except Exception as e:
        return JsonResponse({"message":"Shipment was not deleted"}, status=400)





@login_required(login_url="/users/login")
def create_shipment_location(request):
    if request.method == "POST":
        form= AddLocationForm(request.POST)
        if form.is_valid():
            
            status  = form.cleaned_data.get("status")
            remark = form.cleaned_data.get("remark")
            location = form.cleaned_data.get("location")
            shipment_id = form.data.get("shipment_id")[0]

            location = Location.objects.create(location=location, remark=remark,status=status, shipment = Shipment.objects.get(id=shipment_id))
            messages.success(request, "Shipment Location Created Successfully")
            return redirect(reverse("shipment_detail",kwargs={"pk":int(shipment_id)}))


    return render(request, "users/auth/shipment-details.html", {"addLocationForm":form})