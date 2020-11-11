from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Instytution, Donation, Category
from django.views import View
from django.core.paginator import Paginator
from .forms import CreateUserForm
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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
            "bag": bag,
            "instytution_count": instytution_count,
            "fundations": paginations(self, request)[0],
            "organizations": paginations(self, request)[1],
            "collections": paginations(self, request)[2],
        }
        return render(request, "index.html", ctx)


class FormView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        instytutions = Instytution.objects.all()
        ctx = {
            "categories": categories,
            "instytutions": instytutions,
        }
        return render(request, "form.html", ctx)

    def post(self, request):
        categories = request.POST.getlist('categories')
        bags = request.POST.get('bags')
        organization_id = request.POST.get('organization')
        adress = request.POST.get('address')

        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        data = request.POST.get('data')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')
        donation = Donation.objects.create(quantity=int(bags),
                                           institution=Instytution.objects.get(id=organization_id), user=request.user,
                                           address=adress, city=city, zip_code=postcode, pick_up_date=data,
                                           pick_up_time=time, phone_number=phone, pick_up_comment=more_info)
        donation.categories.set(Category.objects.filter(name__in=categories))
        return redirect('/form-confirmation')

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


class UserProfileView(View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by("is_taken")
        return render(request, "user-profile.html", {"donations": donations})
    def post(self, request):
        if 'taken' in request.POST:
            donation = Donation.objects.filter(user=request.user, id=request.POST.get('taken')).update(is_taken=True)
            return redirect('/user')
        if 'notaken' in request.POST:
            donation = Donation.objects.filter(user=request.user, id=request.POST.get('notaken')).update(is_taken=False)
            return redirect('/user')