# Generated by Django 4.2 on 2024-03-26 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("distribution", "0002_circularsettings_message_circularsettings_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="circularsettings",
            options={
                "ordering": ["start_time", "frequency"],
                "verbose_name": "Параметры рассылки",
                "verbose_name_plural": "Параметры рассылки",
            },
        ),
        migrations.RenameField(
            model_name="circularsettings",
            old_name="end_date",
            new_name="end_time",
        ),
        migrations.RenameField(
            model_name="circularsettings",
            old_name="start_date",
            new_name="start_time",
        ),
        migrations.CreateModel(
            name="Logs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время последней попытки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("sent", "Отправлено"),
                            ("failed", "Не удалось отправить"),
                            ("pending", "В ожидании"),
                        ],
                        default="pending",
                        max_length=50,
                        verbose_name="статус попытки",
                    ),
                ),
                (
                    "response",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="ответ почтового сервера",
                    ),
                ),
                (
                    "circular",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="distribution.circularsettings",
                        verbose_name="рассылка",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="distribution.client",
                        verbose_name="клиент рассылки",
                    ),
                ),
            ],
            options={
                "verbose_name": "лог рассылки",
                "verbose_name_plural": "логи рассылки",
            },
        ),
    ]
