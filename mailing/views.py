from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from mailing.models import Client, UserMessage, Mailing


# Create your views here.

def index(request):
    return render(request, 'mailing/base.html')

# Mailing

class MailingDetailView(generic.DetailView):
    model = Mailing
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data
class MailingCreateView(generic.CreateView):
    model = Mailing
    fields = ('name', 'user_message', 'time', 'period', 'status')
    success_url = reverse_lazy('mailing:mailings')


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    fields = ('name', 'user_message', 'time', 'period', 'status')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

class MailingListView(generic.ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылка',
        'text': 'Рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # Model.get_period_display()
        queryset = queryset.filter(is_active=True).order_by('status', 'period', 'name', 'user_message', 'time')
        return queryset

class MailingDraftListView(generic.ListView):
    model = Mailing
    extra_context = {
        'title': 'Неактивные рассылки',
        'text': 'Неактивные рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False).order_by('status', 'period', 'name', 'user_message', 'time')
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

class UserMessageDetailView(generic.DetailView):
    model = UserMessage
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class UserMessageCreateView(generic.CreateView):
    model = UserMessage
    fields = ('title', 'text')
    success_url = reverse_lazy('mailing:usermessages')


class UserMessageUpdateView(generic.UpdateView):
    model = UserMessage
    fields = ('title', 'text')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:usermessage', args=[self.object.pk])


class UserMessageDeleteView(generic.DeleteView):
    model = UserMessage
    success_url = reverse_lazy('mailing:usermessages')

class UserMessageListView(generic.ListView):
    model = UserMessage
    extra_context = {
        'title': 'Сообщения',
        'text': 'Сообщения'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by("title", "text")
        return queryset

class UserMessageDraftListView(generic.ListView):
    model = UserMessage
    extra_context = {
        'title': 'Неактивные сообщения',
        'text': 'Неактивные сообщения'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False).order_by("title")
        return queryset


class ClientListView(generic.ListView):
    model = Client
    extra_context = {
        'title': 'Наши клиенты',
        'text': "Наши клиенты"
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by("name", "email")
        return queryset

class ClientDraftListView(generic.ListView):
    model = Client
    extra_context = {
        'title': 'Неактивные клиенты',
        'text': 'Неактивные клиенты'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=False).order_by("name")
        return queryset


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ('name', 'email', 'comment', 'is_active')
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(generic.UpdateView):
    model = Client
    fields = ('name', 'email', 'comment', 'is_active')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])


class ClientDeleteView(generic.DeleteView):
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

class ClientDetailView(generic.DetailView):
    model = Client
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

    # def get_object(self, queryset=None):
    # def get(self, request, *args, **kwargs):
    #     self.object = super().get_object()
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

            # # Посылаем email, когда счетчик достигнет 100
            # subject = f"Вашу статью прочитали {self.object.count_view} раз!"
            # message_body = f"Количество просмотров статьи {self.object.title} достигло {self.object.count_view}"
            # send_mail(
            # subject,
            # message_body,
            # EMAIL_HOST_USER,
            # [EMAIL_HOST_USER],
            # fail_silently=False,
            # )

