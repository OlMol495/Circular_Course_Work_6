from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from distribution.models import Client


class HomeTemplateView(TemplateView):
    """
    Обработка запроса на отображение главной страницы
    """
    template_name = 'distribution/home.html'
    extra_context = {'title': 'Best Circular Service'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Client.objects.all()[:3]
        return context_data


class ClientCreateView(CreateView):
    model = Client
    fields = ['name', 'email', 'comments']
    success_url = reverse_lazy('distribution:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()

        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    paginate_by = 10


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['name', 'email', 'comments']

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('distribution:client_detail', args=[self.kwargs.get('pk')])

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('distribution:client_list')







