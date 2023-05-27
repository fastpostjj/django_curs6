from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from mailing.models import Client


# Create your views here.

def index(request):
    return render(request, 'mailing/base.html')

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

