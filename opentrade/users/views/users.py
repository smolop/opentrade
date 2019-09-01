from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError

import datetime

from opentrade.api.serializers.users import AccountVerificationSerializer

from opentrade.assets.views.shares import get_common_context

# Models
#from django.contrib.auth.models import User
from opentrade.users.models import User
from opentrade.users.models import Profile
from opentrade.portfolios.models import Portfolio
from opentrade.wallets.models import Wallet

from opentrade.users.forms import SignupForm, SigninForm

from opentrade.taskapp.tasks import send_confirmation_email

from datetime import datetime, timedelta

from opentrade.utils.functions.profile import calculate_age


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:home')
        else:
            context = {'error': 'Invalid credentials!'}
            return render(request, 'users/login.html', context=context)
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users/login.html')

@login_required
def change_pass_view(request):
    if request.POST:
        username = request.user
        old_password = request.POST['old_password']
        user = authenticate(request, username=username, password=old_password)
        if user:
            new_password = request.POST['new_password']
            new_password_confirmation = request.POST['new_password_confirmation']
            if new_password != new_password_confirmation:
                context = {'error': "Passwords don't match" }
                return render(request, 'users/change_password.html', context=context)
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            user = authenticate(request, username=username, password=new_password)
            if user:
                logout(request)
                return redirect('users:login')
            else:
                context = {'error': "Password hadn't changed." }
                return render(request, 'users/change_password.html', context=context)
        else:
            context = {'error': "Invalid credentials." }
            return render(request, 'users/change_password.html', context=context)
    context = get_common_context(request)
    return render(request, 'users/change_password.html', context=context)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        birthdate = request.POST['birthdate']
        currency = request.POST['currency']
        #import pdb;pdb.set_trace()
        print(birthdate)
        user_age = calculate_age(
            datetime.strptime(
                birthdate,
                "%Y-%M-%d"
                ).date()
            )
        if user_age < 18:
            context = {'error': "Sorry, the account couldn't be created", 'user': 'invalid'}
            return render(request, 'users/register.html', context=context)
        if password != password_confirmation:
            context = {'error': "Passwords don't match" }
            return render(request, 'users/register.html', context=context)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            print("USER SAVED")
        except IntegrityError:
            context = {
                'error': 'Invailid username'
            }
            return render(request, 'users/register.html', context=context)

        wallet = Wallet(init_amount=40000.0, amount=40000.0)
        portfolio = Portfolio()

        wallet.save()
        portfolio.save()

        import pdb
        #pdb.set_trace()
        profile = Profile(
            user=user,
            birthdate=birthdate,
            currency=currency,
            portfolio=portfolio,
            wallet=wallet
        )
        profile.save()
        send_confirmation_email(user_pk=user.pk)
        #return render(request, 'users/register.html', context=context)
        return render(request, 'users/verify.html')
    return render(request, 'users/register.html')

def verify_view(request):
    if request.method == 'POST':
        if not request.POST['_token_']:
            return render(request, 'users/verify.html')
        token = request.POST['_token_']
        data = {'token': token}
        serializer = AccountVerificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
                'message': 'Congratulation!, now you can improve your trading skills!'
            }
        return render(request, 'users/login.html', context=context)
    return render(request, 'users/verify.html')

class SigninView(FormView, LoginRequiredMixin):
    """Login view."""

    template_name = 'users/login.html'
    form_class = SigninForm
    success_url = reverse_lazy('home')

class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        self.objects = form.save()
        return super().form_valid(form)

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/login.html'
