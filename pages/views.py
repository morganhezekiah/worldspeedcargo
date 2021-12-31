from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import os



def index(request):
    return render(request, 'pages/index.html')


def track(request):
    if request.method == "GET":
        return render(request, 'pages/track.html')
    else:
        template_path = 'pdf_temp/track_shipment.html'
        context = {'myvar': 'this is your template context'}
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
    

