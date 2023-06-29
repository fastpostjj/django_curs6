from django.db import models

from user_auth.models import User

from config.settings import NULLABLE


# Create your models here.


class Client(models.Model):
    """
    Клиент сервиса:
    контактный email,
    ФИО,
    комментарий,
    статус.
    """
    name = models.CharField(max_length=150,
                            verbose_name='Фамилия, имя, отчество',
                            )
    email = models.CharField(max_length=150, )
    comment = models.CharField(max_length=150, )
    is_active = models.BooleanField(default=True, verbose_name='активный')
    user = models.ForeignKey(User,
                             verbose_name='автор',
                             default=None,
                             on_delete=models.SET_NULL,
                             **NULLABLE)

    def __str__(self):
        return f"Клиент {self.name}, email:{self.email}, " \
               + "активный" if self.is_active else "неактивный"

    class Meta():
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)
        permissions = {
            ("set_client_status", "can change client status")
        }


class UserMessage(models.Model):
    """
    Сообщение для рассылки:
    тема письма,
    тело письма,
    статус.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок сообщения'
    )
    text = models.CharField(
        max_length=500,
        verbose_name='Текст сообщения'
    )
    is_active = models.BooleanField(default=True, verbose_name='активный')
    user = models.ForeignKey(User,
                             verbose_name='автор',
                             default=None,
                             on_delete=models.SET_NULL,
                             **NULLABLE)

    def __str__(self):
        return f"Текст заголовка: {self.title}." # + " Текст сообщения: {self.text}"  # + "активное" if self.is_active else "неактивное"

    class Meta():
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title', 'text')


class Mailing(models.Model):
    """
    Рассылка (настройки):
    название,
    время рассылки;
    периодичность: раз в день, раз в неделю, раз в месяц;
    статус рассылки (завершена, создана, запущена),
    статус активности.
    """
    name = models.CharField(verbose_name='Название рассылки', max_length=100, default='Новая рассылка')
    user_message = models.ForeignKey(
        UserMessage,
        verbose_name="Сообщение",
        on_delete=models.SET_NULL,
        **NULLABLE
    )
    time = models.TimeField(
        verbose_name="Время рассылки",
        default="0:00:00"

    )
    period = models.CharField(
        verbose_name="Периодичность рассылки",
        max_length=12,
        choices=[
            ('daily', 'раз в день'),
            ('weekly', 'раз в неделю'),
            ('monthly', 'раз в месяц')
        ],
        default='monthly'
    )
    start_day = models.DateField(
        verbose_name="Дата начала рассылки",
        default="2001-01-01"
    )

    status = models.CharField(
        verbose_name="Статус рассылки",
        max_length=9,
        choices=[
            ("finished", "завершена"),
            ("created", "создана"),
            ("run", "запущена")
        ],
        default="created"
    )
    is_active = models.BooleanField(default=True, verbose_name='активная')
    user = models.ForeignKey(User,
                             verbose_name='автор',
                             default=None,
                             on_delete=models.SET_NULL,
                             **NULLABLE)


    def __str__(self):
        period = (dict(self._meta.get_field('period').choices)[self.period])
        status = (dict(self._meta.get_field('status').choices)[self.status])
        return f" {self.name}->Сообщение:{self.user_message.title}, время: {self.time}, периодичность: {period}, "# \
               # + f"статус: {status}, " + "активная" if self.is_active else "неактивная"

    class Meta():
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('is_active', 'time', 'period', 'status',)
        permissions = {
            ("set_mailing_status", "can change mailing status")
        }


class MailingAttempts(models.Model):
    """
    Попытка рассылки:
    дата и время последней попытки;
    статус попытки;
    ответ почтового сервера, если он был.
    """
    mayling = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        on_delete=models.CASCADE
    )
    mailing_daytime = models.DateTimeField(
        verbose_name="Дата и время последней попытки",
        **NULLABLE
    )
    server_answer = models.CharField(
        max_length=200,
        verbose_name="Ответ почтового сервера",
        **NULLABLE
    )
    status = models.CharField(
        max_length=14,
        verbose_name='Статус рассылки',
        choices=[
            ('successfully', 'успешно'),
            ('unsuccessfully', 'неудачно')],
        **NULLABLE
    )
    is_active = models.BooleanField(default=True, verbose_name='активная')

    def __str__(self):
        status = None
        if self.status:
            status = (dict(self._meta.get_field('status').choices)[self.status])
        return f"Попытка рассылки-> Дата и время: {self.mailing_daytime}, статус: {status}, ответ сервера: {self.server_answer}, " \
               + "активная" if self.is_active else "неактивная"

    class Meta():
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ('mailing_daytime', 'server_answer')
