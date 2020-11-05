from django.shortcuts import render

from .models import Instytution, Donation, Category
from django.views import View
# Create your views here.





class IndexView(View):
    def get(self, request):
        donations = Donation.objects.all()
        bag = 0
        instytutions = Instytution.objects.all()
        instytution_count = instytutions.count()
        fundations = instytutions.filter(type=0)[:3]
        organizations = instytutions.filter(type=1)[:3]
        collections = instytutions.filter(type=2)[:3]
        for donat in donations:
            bag = donat.quantity + bag
        ctx = {
            "bag":bag,
            "instytution_count": instytution_count,
            "fundations": fundations,
            "organizations": organizations,
            "collections": collections,
        }
        return render(request, "index.html", ctx)

class FormView(View):
    def get(self, request):
        return render(request, "form.html", )

class FormConfirView(View):
    def get(self, request):
        return render(request, "form-confirmation.html", )

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", )


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", )