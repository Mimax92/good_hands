from django.shortcuts import render

from .models import Instytution, Donation, Category
from django.views import View
from django.core.paginator import Paginator
from .forms import CreateUserForm
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.shortcuts import redirect

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
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/register')


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        ctx = {
            "form": form
        }
        return render(request, "register.html", ctx)
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("repeated_password")
            user = get_user_model().objects.create_user(**form.cleaned_data)
            return redirect("/login")
        return render(request, "register.html", {"form": form})

