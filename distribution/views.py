from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from distribution.forms import CircularForm, MessageForm, ClientForm
from distribution.models import Client, CircularSettings, Message


class OwnerSuperuserMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class HomeTemplateView(TemplateView):
    """ Обработка запроса на отображение главной страницы """
    template_name = 'distribution/home.html'
    extra_context = {'title': 'Best Circular Service'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Message.objects.all()[:3]
        context_data['circular_count'] = CircularSettings.objects.count()
        context_data['unique_clients_count'] = Client.objects.count()
        return context_data


class CircularCreateView(PermissionRequiredMixin, CreateView):
    model = CircularSettings
    form_class = CircularForm
    permission_required = 'main.add_circular_settings'
    success_url = reverse_lazy('distribution:circular_list')

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            new_circular = form.save(commit=False)
            new_circular.owner = self.request.user
            new_circular.status = CircularSettings.Status.CREATED
            new_circular.save()
        return super().form_valid(form)


class CircularListView(ListView):
    model = CircularSettings
    login_url = 'users:login'
    extra_context = {
        'title': 'Список рассылок',
    }
    paginate_by = 5

class CircularDetailView(DetailView):
    model = CircularSettings

    extra_context = {
        'title': 'Детали рассылки',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        circular_data = []
        clients_data = self.object.clients.values('name', 'email', 'comments')
        circular_data.append({'clients_data': clients_data})
        context['circular_data'] = circular_data

        message_title = None
        if self.object.message:
            message_title = self.object.message.title

        context['message_title'] = message_title
        return context


class CircularUpdateView(UserPassesTestMixin, UpdateView):
    model = CircularSettings
    form_class = CircularForm

    extra_context = {
        'title': 'Редактирование рассылки',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('distribution:circular_detail', args=[self.object.pk])

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return self.request.user == CircularSettings.objects.get(pk=self.kwargs['pk']).owner


class CircularDeleteView(DeleteView):
    model = CircularSettings
    success_url = reverse_lazy('distribution:mailings_list')

    extra_context = {
        'title': 'Удаление рассылки',
    }


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:message_list')
    extra_context = {
        'title': 'Создание письма',
    }


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    login_url = 'users:login'
    extra_context = {
        'title': 'Тексты рассылок',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            queryset = Message.objects.all()
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageDetailView(OwnerSuperuserMixin, DetailView):
    model = Message
    extra_context = {
        'title': 'Просмотр письма',
    }


class MessageUpdateView(OwnerSuperuserMixin, UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {
        'title': 'Редактирование письма',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('distribution:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(OwnerSuperuserMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('distribution:mail_list')
    extra_context = {
        'title': 'Удаление письма',
    }


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Новый клиент',
    }
    success_url = reverse_lazy('distribution:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    paginate_by = 10
    permission_required = 'distribution.view_client'
    login_url = 'users:login'
    extra_context = {
        'title': 'Список клиентов',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            queryset = Client.objects.all()
            return queryset
        else:
            raise Http404


class ClientDetailView(OwnerSuperuserMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Данные клиента',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Изменение данных клиента',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise Http404
        return self.object

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('distribution:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(OwnerSuperuserMixin, DeleteView):
    model = Client
    extra_context = {
        'title': 'Удаление клиента',
    }
    success_url = reverse_lazy('distribution:client_list')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'distribution/contact.html', context)
