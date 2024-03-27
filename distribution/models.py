from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email = models.EmailField(verbose_name='Имейл')
    comments = models.TextField(**NULLABLE, verbose_name='Сообщение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь-владелец', **NULLABLE)

    def __str__(self):
        return f"{self.name}: {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['email']


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель сообщения', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['title',]


class CircularSettings(models.Model):

    class Status(models.TextChoices):
        CREATED = 'Создана', 'created'
        IN_PROGRESS = 'Запущена', 'in-progress'
        COMPLETED = 'Завершена', 'completed'
        CANCELLED = 'Отменена', 'cancelled'

    class Frequency(models.TextChoices):
        DAILY = 'Д', 'daily'
        WEEKLY = 'Н', 'weekly'
        MONTHLY = 'М', 'monthly'

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    start_time = models.DateField(verbose_name='начало')
    end_time = models.DateField(verbose_name='окончание', **NULLABLE)
    frequency = models.CharField(max_length=2, choices=Frequency.choices,
                                 default=Frequency.DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED,
                              verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='Получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Менеджер рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.start_time}, {self.end_time}, {self.frequency}, {self.status}"

    class Meta:
        verbose_name = 'Параметры рассылки'
        verbose_name_plural = 'Параметры рассылки'
        ordering = ['start_time', 'frequency', ]



class Logs(models.Model):

    SENT = 'sent'
    FAILED = 'failed'
    PENDING = 'pending'

    STATUS = [
        (SENT, 'Отправлено'),
        (FAILED, 'Не удалось отправить'),
        (PENDING, 'В ожидании')
    ]

    date = models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки')
    status = models.CharField(max_length=50, choices=STATUS, default=PENDING, verbose_name='статус попытки')
    response = models.CharField(max_length=250, verbose_name='ответ почтового сервера', **NULLABLE)

    circular = models.ForeignKey(CircularSettings, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.date} - {self.status}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
