from django.shortcuts import render

from .models import Instytution, Donation, Category
from django.views import View
from django.core.paginator import Paginator
# Create your views here.


def paginations(self, request):
    instytutions = Instytution.objects.all()
    fundations = instytutions.filter(type=0)
    organizations = instytutions.filter(type=1)
    collections = instytutions.filter(type=2)
    paginator_f = Paginator(fundations, 3)
    paginator_o = Paginator(organizations, 3)
    paginator_c = Paginator(collections, 3)
    page_f = request.GET.get('page-f')
    page_o = request.GET.get('page-o')
    page_c = request.GET.get('page-c')
    fundations = paginator_f.get_page(page_f)
    organizations = paginator_o.get_page(page_o)
    collections = paginator_c.get_page(page_c)
    return [fundations, organizations, collections]


class IndexView(View):
    def get(self, request):
        donations = Donation.objects.all()
        bag = 0
        instytutions = Instytution.objects.all()
        instytution_count = instytutions.count()
        for donat in donations:
            bag = donat.quantity + bag
        ctx = {
            "bag":bag,
            "instytution_count": instytution_count,
            "fundations": paginations(self, request)[0],
            "organizations": paginations(self, request)[1],
            "collections": paginations(self, request)[2],
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