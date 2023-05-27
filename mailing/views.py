from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from mailing.models import Client, UserMessage


# Create your views here.

def index(request):
    return render(request, 'mailing/base.html')

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
            # subject = "Клиент деактивирован"
            # message_body = f"Клиент {client} деактивирован"
        else:
            client.is_active = True
            # subject = "Клиент активирован"
            # message_body = f"Клиент {client} активирован"
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

