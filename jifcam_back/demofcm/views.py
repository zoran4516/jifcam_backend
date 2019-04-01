from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from fcm_django.models import FCMDevice

# Create your views here.

class DemoView(View):

    def get(self, request):
        return render(request, "demofcm/index.html")

    def post(self, request):
        device = FCMDevice.objects.all().first()

        device.send_message(title="Title", body="Message")
        return HttpResponse('Reply')
