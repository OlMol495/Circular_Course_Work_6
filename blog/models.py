from django.db import models
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}

class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, verbose_name='Slug', unique=True)
    text = models.TextField(verbose_name='Текст', **NULLABLE)
    preview_image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='картинка')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание поста', **NULLABLE)
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования', **NULLABLE)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
