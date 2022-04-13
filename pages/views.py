from django.contrib import messages
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa
from django.http import HttpResponse
import os
from locations.models import Location

from users.models import Shipment


def index(request):
    return render(request, 'pages/index.html')

def sitemap(request):
    return render(request, "pages/sitemap.xml", content_type ="application/xhtml+xml")

def track(request):
    if request.method == "GET":
        return render(request, 'pages/track.html')
    else:
        trackingUUID = request.POST.get("trackingUUID")
        try:
            s = Shipment.objects.get(uuid=trackingUUID)
            
        except:
            messages.error(request,"Result Not found")
            return redirect("/track")
        
        request.session['shipment_invoice_uuid']  = trackingUUID
        return redirect(reverse("track_shipment_details", kwargs={"pk":s.pk}))
        
def track_shipment_details(request, pk):
    try:
        s = Shipment.objects.get(id=pk)
    except Shipment.DoesNotExist as e:
        return HttpResponse("Shipment with this ID does not exist")
    locations  = Location.objects.filter(shipment=s)
    l = locations.order_by("-id")
    counter = 0
    splashArray =[]
    while counter < 4:
        try:
            splashArray.append(locations[counter])
        except Exception as e:
            pass
        counter+=1
    
    locationForSplash = splashArray
    return render(request, 'pages/track_shipment_details.html' , {"shipment":s,"location":l,"locationForSplash":locationForSplash})

        
def download_shipment_invoice(request):
    trackingUUID = request.session['shipment_invoice_uuid'] 
    s = Shipment.objects.get(uuid=trackingUUID)
    template_path = 'pdf_temp/track_shipment.html'
    context = {'shipment':  s}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shipment.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def trackPDF(request):
    pass
    

