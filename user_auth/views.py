from random import sample

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View, generic
from django.views.generic import CreateView, UpdateView, TemplateView

from user_auth.forms import UserForgotPasswordForm, UserRegisterForm, UserSetNewPasswordForm, UserForm
from user_auth.models import User


# Create your views here.
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class UsersListView(LoginRequiredMixin, generic.ListView):
    model = User
    extra_context = {
        'title': 'Пользователи сервиса',
        'text': 'Пользователи сервиса'
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by('email', 'phone', 'is_active')
        return queryset

class UsersDraftListView(LoginRequiredMixin, generic.ListView):
    model = User
    extra_context = {
        'title': 'Пользователи сервиса',
        'text': 'Пользователи сервиса'
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False).order_by('email', 'phone', 'is_active')
        return queryset

class UserIsNotAuthenticated(UserPassesTestMixin):
    """Миксин для запрета регистрации авторизованных юзеров"""
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('home')

class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'user_auth/user_password_reset.html'
    success_url = reverse_lazy('mailing:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'user_auth/email/password_subject_reset_mail.txt'
    email_template_name = 'user_auth/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'user_auth/user_password_set_new.html'
    success_url = reverse_lazy('products:index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context

class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user_auth:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('user_auth:email_confirmed')
        else:
            return redirect('user_auth:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'user_auth/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'user_auth/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'user_auth/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context
class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('mailing:index')
    template_name = 'user_auth/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('user_auth:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = get_current_site(self.request)
        domain = current_site.domain
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{domain}{activation_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return redirect('user_auth:email_confirmation_sent')

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('mailing:index')
    template_name = 'user_auth/register.html'

    def form_valid(self, form):
        new_user = form.save()
        # verification_link = _make_hash_value(request.user)

        verification_kod = "".join(sample("".join([str(i) for i in range(0,10)]), 4))

        verification_link=""
        message = f"""Для завершения регистрации пройдите
        по следующей ссылке, чтобы подтвердить свой
        адрес электронной почты: < a href = "{{ verification_link }}" > Подтвердить < / a >"""

        send_mail(
            subject='Вы начали процедуру регистрации',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

def generate_new_password(request):
    password = "".join(sample("".join([str(i) for i in range(0,10)]) + "*+-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 10))
    request.user.set_password(password)
    request.user.save()
    send_mail(
        subject='Новый пароль',
        message=f'Вам установлен новый пароль:\n{password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('user_auth:login'))






