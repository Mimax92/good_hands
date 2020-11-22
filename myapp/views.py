from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Instytution, Donation, Category, CustomUser
from django.views import View, generic
from django.core.paginator import Paginator
from .forms import CreateUserForm, UserChangeForm
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .utils import Util, account_activation_token
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from validate_email import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import re
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

def passwordValidation(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        return True
    else:
        return False

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


def validationForm(request, bags, adress, city, postcode, phone, more_info, data, time):
    arr_true_false = []
    if int(bags) < 0 or bags == "":
        messages.error(request, " Liczba worków musi być większa niż 0")
        arr_true_false.append(1)
    if len(adress) > 200 or len(adress) < 0 or adress == "":
        messages.error(request, " Za długi lub adres lub adres nie podany")
        arr_true_false.append(1)
    if len(city) > 50 or len(city) < 0 or city == "":
        messages.error(request, " Za długa nazwa miasta lub brak nazwy")
        arr_true_false.append(1)
    if len(postcode) > 6 or len(postcode) < 0 or postcode == "":
        messages.error(request, " Za długi kod pocztowy lub brak kodu ")
        arr_true_false.append(1)
    if len(phone) < 0 and len(phone) > 9 and any(map(str.isdigit, phone)) or phone == "":
        messages.error(request, "Numer musi składać się z max 9 cyfr")
        arr_true_false.append(1)
    if len(more_info) > 250:
        messages.error(request, "Za długi opis")
        arr_true_false.append(1)
    if data == "" or time == "":
        messages.error(request, "Brak adresu lub Godziny odbioru")
        arr_true_false.append(1)
    if arr_true_false == []:
        return True
    else:
        return False


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
        if validationForm(request, bags, adress, city, postcode, phone, more_info, data, time):
            donation = Donation.objects.create(quantity=int(bags),
                                               institution=Instytution.objects.get(id=organization_id),
                                               user=request.user,
                                               address=adress, city=city, zip_code=postcode, pick_up_date=data,
                                               pick_up_time=time, phone_number=phone, pick_up_comment=more_info)
            donation.categories.set(Category.objects.filter(name__in=categories))
            return redirect('/form-confirmation')
        else:
            return redirect('/form#alert')


class FormConfirView(LoginRequiredMixin, View):
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
            password = form.cleaned_data["password"]
            repeated_password = form.cleaned_data["repeated_password"]
            if passwordValidation(password) and password == repeated_password:
                form.cleaned_data.pop("repeated_password")
                user = get_user_model().objects.create_user(**form.cleaned_data)
                user.is_active = False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request).domain
                relativeLink = reverse('emailverify',
                                       kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                activate_url = "http://" + current_site + relativeLink
                email_body = "Cześć " + user.first_name + " Kliknij w link poniżej celem veryfikacji adresu email \n" + activate_url
                data = {
                    'email_body': email_body,
                    'to_email': user.email,
                    'email_subject': 'Zweryfikuj swój Email'
                }
                Util.send_email(data)
                messages.success(request, 'Na adres email został wysłany link aktywacyjny')
                return redirect("/login")
            messages.info(request, 'Hasło nie spełnia wymagań lub się od siebie różnią')
            return render(request, "register.html", {"form": form})
        return render(request, "register.html", {"form": form})


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                return redirect("/login" + '?message=' + 'User already activated')
            if user.is_active:
                return redirect("/login")
            user.is_active = True
            user.save()
            messages.success(request, 'Konto aktywowane pomyślnie')
            return redirect("/login")
        except Exception as ex:
            return redirect("/register")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by("is_taken", "-don_creation")
        return render(request, "user-profile.html", {"donations": donations})

    def post(self, request):
        if 'taken' in request.POST:
            donation = Donation.objects.filter(user=request.user, id=request.POST.get('taken')).update(is_taken=True)
            return redirect('/user')
        if 'notaken' in request.POST:
            donation = Donation.objects.filter(user=request.user, id=request.POST.get('notaken')).update(is_taken=False)
            return redirect('/user')


@login_required
def updateuserprofileview(request):
    if request.method == 'POST' and 'dat' in request.POST:
        form = UserChangeForm(request.POST, instance=request.user)
        password = request.POST.get('password')
        user = authenticate(request, email=request.user.email, password=password)
        if form.is_valid():
            if user is not None:
                form.save()
                return redirect('/update-user')
            else:
                messages.error(request, "Złe hasło")
                return redirect('/update-user')
        else:
            return redirect('/update-user')

    if request.method == 'POST' and 'pas' in request.POST:
        form_password = PasswordChangeForm(data=request.POST, user=request.user)
        if form_password.is_valid():
            form_password.save()
            messages.error(request, "Nowa hasło ustawione")
            return redirect('/login/')
        else:
            return redirect('/update-user')
    else:
        form = UserChangeForm(instance=request.user)
        form_password = PasswordChangeForm(user=request.user)
        return render(request, "registration/edit_profile.html", {"form": form, "form_password": form_password})

class RequestPasswordResetEmailView(View):
    def get(self, request):
        return render(request, 'reset-password.html')

    def post(self, request):
        email=request.POST['email']

        ctx = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, "Proszę podać właściwy adres email")
            return render(request, 'reset-password.html', ctx)

        user=CustomUser.objects.filter(email=email)
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            current_site = get_current_site(request).domain
            relativeLink = reverse('reset-user-password',
                                   kwargs={'uidb64': uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})
            reset_url = "http://" + current_site + relativeLink
            email_body = "Cześć " + user[0].first_name + " Aby zresetować hasło kliknij w link poniżej \n" + reset_url
            data = {
                'email_body': email_body,
                'to_email': user[0].email,
                'email_subject': 'Reset hasła'
            }
            Util.send_email(data)

            messages.success(request, 'Wysłaliśmy Ci maila celem resetu hasła')

            return render(request, 'reset-password.html')
        messages.success(request, 'Nie ma konta powiązanego z tym adresem email')
        return render(request, 'reset-password.html')
class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        ctx = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Link został już wykorzystany")
                return render(request, 'reset-password.html')
        except Exception as identifier:
            pass
        return render(request, 'set-new-password.html', ctx)
    def post(self, request, uidb64, token):
        ctx = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Hasła są różne')
            return render(request, 'set-new-password.html', ctx)
        if len(password) < 8:
            messages.error(request, "Hasło za krótkie")
            return render(request, 'set-new-password.html', ctx)
        if passwordValidation(password) == False:
            messages.error(request, "Hasło za musi zawierać wielkie litery, małe litery, cyfry i znaki specjalne")
            return render(request, 'set-new-password.html', ctx)
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Hasło zmienione pomyślnie, może się zalogować za pomocą nowego hasła :)")
            return redirect('/login/')
        except Exception as identifier:
            # import pdb
            # pdb.set_trace()
            messages.info(request, "coś poszło nie tak :(")
            return render(request, 'set-new-password.html', ctx)

        # return render(request, 'set-new-password.html', ctx)

