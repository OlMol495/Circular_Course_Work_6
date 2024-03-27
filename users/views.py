from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from config import settings
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, FormView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login


def send_email_verify(request, user):
    current_site = get_current_site(request)
    context = {"user": user, "domain": current_site.domain, "uid": urlsafe_base64_encode(force_bytes(user.pk)),
               "token": default_token_generator.make_token(user)}
    message = render_to_string("users/email_verify.html", context)
    email = EmailMessage(subject="Verification", body=message, to=[user.email])
    email.send()


class EmailVerifyView(View):
    def get(self, request, uidb64=None, token=None):
        user = self.get_user_by_uidb64(uidb64)
        print(user)
        print(user.token)
        if user is not None and user.token == token:
            user.email_confirmed = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('distribution:home')
        else:
            return redirect(reverse('users:login'))

    @staticmethod
    def get_user_by_uidb64(uidb64):
        uid = urlsafe_base64_decode(uidb64)
        uid_str = force_str(uid)
        user = User.objects.get(pk=int(uid_str))
        return user


class UserLoginView(LoginView):
    model = User
    template_name = 'users/login.html'
    success_url = reverse_lazy('distribution:home')

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        verify_token = default_token_generator.make_token(user)
        user.token = verify_token
        user.is_active = False
        user.save()
        self.send_email_verify(self.request, user, verify_token)

        return super().form_valid(form)

    @staticmethod
    def send_email_verify(request, user, token):
        current_site = get_current_site(request)
        user.save()
        context = {"user": user, "domain": current_site.domain, "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                   "token": token}
        message = render_to_string("users/email_verify.html", context)
        email = EmailMessage(subject="Verification", body=message, to=[user.email])
        email.send()


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Смена пароля в BestStoreEver',
        message=f'Ваш новый пароль для BestStoreEver: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    messages.success(request, 'Вам на почту отправлено письмо с новым паролем')
    return redirect(reverse('distribution:home'))


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('users/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)

        try:
            user = User.objects.get(email=email)
            new_password = User.objects.make_random_password()
            send_mail(
                subject='Смена пароля в BestStoreEver',
                message=f'Ваш новый пароль для BestStoreEver: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            messages.success(request, 'Вам на почту отправлено письмо с новым паролем')
            user.set_password(new_password)
            user.save()
            return redirect(reverse('distribution:home'))

        except Exception as e:
            message = f"Пользователь с такими имейлом не найден"
            context = {'message': message}
            return render(request, 'users/forgot_password.html', context)

    else:
        return render(request, 'users/forgot_password.html')




# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import reverse_lazy
# from django.views.generic import CreateView, UpdateView
#
# from users.forms import UserRegisterForm, UserProfileForm, LoginViewForm
# from users.models import User
#
#
# class UserLoginView(LoginView):
#     model = User
#     form_class = LoginViewForm
#     template_name = 'users/login1.html'
#     extra_context = {
#         'title': 'Вход',
#     }
#     success_url = reverse_lazy('distribution:home')
#
#
# class RegisterView(CreateView):
#     model = User
#     form_class = UserRegisterForm
#     template_name = 'users/register1.html'
#     success_url = reverse_lazy('users:login')
#
#
# class UserLogoutView(LogoutView):
#     success_url = reverse_lazy('users/login1.html')
#
#
# class ProfileView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     success_url = reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user