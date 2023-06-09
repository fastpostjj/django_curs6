from django import forms

from mailing.models import UserMessage, Client, Mailing, UserMessage


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        if 'is_active' in self.fields:
            # Задаем класс для кнопки "Активный"
            self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
            self.fields['is_active'].label_attrs = {'class': 'form-check-label'}


class UserMessageForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = UserMessage
        # fields = '__all__'
        exclude = ['user', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 100%;height: 200px;', 'rows': 10, }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field_name, field in self.fields.items():
        #     field.widget.attrs['class'] = 'form-control'


class ClientForm(FormStyleMixin, forms.ModelForm):
    # Форма для админа
    class Meta:
        model = Client
        fields = '__all__'
        # exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ClientFormCut(FormStyleMixin, forms.ModelForm):
    # Форма для обычного пользователя и стаффа
    class Meta:
        model = Client
        fields = '__all__'
        # exclude = ['user',]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Поля недоступны для редактирования
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['comment'].widget.attrs['readonly'] = True
        # self.fields['user'].widget.attrs['readonly'] = True
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            # Если нет, то скрываем поле user
            self.fields['user'].widget = forms.HiddenInput()

class MailingForm(FormStyleMixin, forms.ModelForm):
    # Форма для пользователя и админа
    class Meta:
        model = Mailing
        fields = '__all__'
        # exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MailingFormCut(FormStyleMixin, forms.ModelForm):
    # Форма для стаффа
    class Meta:
        model = Mailing
        # fields = '__all__'
        exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # status и is_active доступны для редактирования
        # Поля недоступны для редактирования:
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['user_message'].widget.attrs['readonly'] = True
        self.fields['time'].widget.attrs['readonly'] = True
        self.fields['period'].widget.attrs['readonly'] = True
        self.fields['start_day'].widget.attrs['readonly'] = True
        # self.fields['user'].widget.attrs['readonly'] = True
        self.fields['client'].widget.attrs['readonly'] = True


class UserMessageForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = '__all__'
        # exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserMessageFormCut(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = UserMessage
        # fields = '__all__'
        exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Поля недоступны для редактирования:
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
        # self.fields['name'].widget.attrs['readonly'] = True
        # self.fields['user_message'].widget.attrs['readonly'] = True
        # self.fields['time'].widget.attrs['readonly'] = True
        # self.fields['period'].widget.attrs['readonly'] = True
        # self.fields['start_day'].widget.attrs['readonly'] = True
        # self.fields['user'].widget.attrs['readonly'] = True



