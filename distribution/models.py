from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email = models.EmailField(verbose_name='Имейл')
    comments = models.TextField(**NULLABLE, verbose_name='Сообщение')

    def __str__(self):
        return f"{self.name}: {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['email']


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

    start_date = models.DateField(verbose_name='начало')
    end_date = models.DateField(verbose_name='окончание', **NULLABLE)
    frequency = models.CharField(max_length=2, choices=Frequency.choices,
                                 default=Frequency.DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED,
                              verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='Получатели')

    def __str__(self):
        return f"{self.start_date}, {self.end_date}, {self.frequency}, {self.status}"

    class Meta:
        verbose_name = 'Параметры рассылки'
        verbose_name_plural = 'Параметры рассылки'
        ordering = ['start_date', 'frequency', ]


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['title',]

