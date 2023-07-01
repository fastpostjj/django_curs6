import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from mailing.forms import ClientForm, ClientFormCut, MailingForm, MailingFormCut, UserMessageForm, UserMessageFormCut
from mailing.models import Client, UserMessage, Mailing, MailingAttempts
from blog.models import Blog
from mailing.services.send_mailing import find_malling_for_send


# Create your views here.

def index(request):
    return render(request, 'mailing/base.html')

def home(request):
    # Главная страница
    """
    - количество рассылок всего
    - количество активных рассылок
    - количество уникальных клиентов для рассылок
    - 3 случайные статьи из блога
    """
    size = 3
    objects = Blog.objects.filter(is_published=True, is_active=True).order_by('?')[:size]

    return render(request, 'mailing/home.html',
        {
        'text':'Добро пожаловать!',
        'mailing_count': len(Mailing.objects.all()),
        'mailing_active_count': len(Mailing.objects.filter(is_active=True)),
        'unique_count': Client.objects.values('email').annotate(total=Count('email')).count(),
        'blog_random': objects
        })


# MailingAttempts
class MailingAttemptsDetailView(LoginRequiredMixin, generic.DetailView):
    model = MailingAttempts
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class MailingAttemptsListView(LoginRequiredMixin, generic.ListView):
    model = MailingAttempts
    extra_context = {
        'title': 'Попытки рассылки',
        'text': 'Попытки рассылки'
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by('-mailing_daytime', 'mayling', 'server_answer', 'status', 'is_active')
        return queryset

# Mailing

class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    fields = ('name', 'user_message', 'time', 'start_day', 'period', 'status', 'client')
    success_url = reverse_lazy('mailing:mailings')

    def form_valid(self, form):
        """Текущий пользователь будет автором созданной рассылки"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        # Запускаем все активные рассылки
        find_malling_for_send()
        return redirect(self.get_success_url())


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    fields = ('name', 'user_message', 'time', 'start_day', 'period', 'status', 'client')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser or self.object.user == request.user):
            context = {'text': 'Ошибка!',
                       'error_message': 'Вносить изменения в рассылку, может только пользователь, который ее создал или администратор!'}
            return render(request, 'mailing/error.html', context)
        return super().get(request, args, kwargs)

    def get_form_class(self, *args, **kwargs):
        # Редактирование формы доступно только админу и  автору. Менеджеру с правами is_staff доступно только изменение поля is_active
        if self.request.user.is_superuser:
             class_form = MailingForm
        elif self.object.user == self.request.user:
            class_form = MailingForm
        elif self.request.user.is_staff:
             class_form = MailingFormCut
        else:
             class_form = None
        return class_form

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('user')
        return form


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылка',
        'text': 'Рассылки'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть все рассылки
            queryset = queryset.filter(is_active=True).order_by('status', 'period', 'name', 'user_message', 'time')
        else:
            # Обычный пользователь - только свои
            queryset = queryset.filter(is_active=True, user=self.request.user).order_by('status', 'period', 'name', 'user_message', 'time')
        return queryset

class MailingDraftListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    extra_context = {
        'title': 'Неактивные рассылки',
        'text': 'Неактивные рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False, user=self.request.user).order_by('status', 'period', 'name', 'user_message', 'time')
        return queryset
class MailingRunListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    extra_context = {
        'title': 'Запущенные рассылки',
        'text': 'Запущенные рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # Админ и стафф видят все рассылки, остальные пользователи- только свои
        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, status='run').order_by('status', 'period', 'name', 'user_message', 'time')
        else:
            queryset = queryset.filter(is_active=True, status='run', user=self.request.user).order_by('status', 'period', 'name', 'user_message', 'time')
        return queryset
class Toggle_Activity_Mailing(View):
    def get(request, *args, pk, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.is_active:
            mailing.is_active = False
        else:
            mailing.is_active = True
        mailing.save()
        return redirect(reverse('mailing:mailing', args=[mailing.pk]))

class Toggle_Activity_UserMessage(View):
    def get(request, *args, pk, **kwargs):
        usermessage = get_object_or_404(UserMessage, pk=pk)
        if usermessage.is_active:
            usermessage.is_active = False
        else:
            usermessage.is_active = True
        usermessage.save()
        return redirect(reverse('mailing:usermessage', args=[usermessage.pk]))

class UserMessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserMessage
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class UserMessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserMessage
    fields = ('title', 'text')
    success_url = reverse_lazy('mailing:usermessages')

    def form_valid(self, form):
        """Текущий пользователь будет автором созданного сообщения"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())

class UserMessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserMessage
    fields = ('title', 'text')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:usermessage', args=[self.object.pk])

    def get_form_class(self, *args, **kwargs):
        # Редактирование формы доступно только админу и  пользователю. Менеджеру с правами is_staff редактирование недоступно
        if self.request.user.is_superuser:
             class_form = UserMessageForm
        elif self.object.user == self.request.user:
            class_form = UserMessageForm
        elif self.request.user.is_staff:
             class_form = UserMessageFormCut
        else:
             class_form = UserMessageForm
        return class_form

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('user')
        return form

class UserMessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserMessage
    success_url = reverse_lazy('mailing:usermessages')

class UserMessageListView(LoginRequiredMixin, generic.ListView):
    model = UserMessage
    extra_context = {
        'title': 'Сообщения',
        'text': 'Сообщения'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть все рассылки
            queryset = queryset.filter(is_active=True).order_by("title",)
        else:
            # Обычный пользователь - только своих
            queryset = queryset.filter(is_active=True, user=self.request.user).order_by("title",)
        return queryset
class UserMessageDraftListView(LoginRequiredMixin, generic.ListView):
    model = UserMessage
    extra_context = {
        'title': 'Неактивные сообщения',
        'text': 'Неактивные сообщения'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False).order_by("title")
        return queryset

class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    extra_context = {
        'title': 'Наши клиенты',
        'text': "Наши клиенты"
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть всех клиентов
            queryset = queryset.filter(is_active=True).order_by("name", "email")
        else:
            # Обычный пользователь - только своих
            queryset = queryset.filter(is_active=True, user=self.request.user).order_by("name", "email")
        return queryset

class ClientDraftListView(LoginRequiredMixin, generic.ListView):
    model = Client
    extra_context = {
        'title': 'Неактивные клиенты',
        'text': 'Неактивные клиенты'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False, user=self.request.user).order_by("name")
        return queryset


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    fields = ('name', 'email', 'comment', 'is_active')
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        """Текущий пользователь будет автором созданного клиента"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    fields = ('name', 'email', 'comment', 'is_active')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser or self.object.user == request.user):
            context = {'text':'Ошибка!',
                       'error_message':'Вносить изменения в данные клента, может только пользователь, который его создал или администратор!'}
            return render(request, 'mailing/error.html', context)
        return super().get(request, args, kwargs)

    def get_form_class(self, *args, **kwargs):
        # Редактирование формы доступно только админу и  автору. Менеджеру с правами is_staff доступно только изменение поля is_active
        if self.request.user.is_superuser:
             class_form = ClientForm
        elif self.object.user == self.request.user:
            class_form = ClientForm
        elif self.request.user.is_staff:
             class_form = ClientFormCut
        else:
             class_form = None
        return class_form

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('user')
        return form


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')



class Toggle_Activity_Client(View):
    def get(request, *args, pk, **kwargs):
        text = ""
        client = get_object_or_404(Client, pk=pk)
        if client.is_active:
            client.is_active = False
        else:
            client.is_active = True
        client.save()

        return redirect(reverse('mailing:client', args=[client.pk]))

class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

    # def get_object(self, queryset=None):
    def get(self, request, *args, **kwargs):
        self.object = super().get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



