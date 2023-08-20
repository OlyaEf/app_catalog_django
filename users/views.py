import random
import string

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.save()

        # Создаем и сохраняем токен подтверждения
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        new_user.email_verification_token = token
        new_user.save()

        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = ('Подтвердите ваш аккаунт. '
                        'Пройдите по этой ссылке для подтверждения регистрации:')
        message = render_to_string(
            'users/verify_email.html',
            {
                'user': new_user,
                'domain': current_site.domain,
                'token': token,
                'uid': new_user.pk,
            },
        )
        send_mail(mail_subject, message, 'noreply@localhost', [new_user.email])
        return response


class VerifyEmailView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.email_verified = True
            user.save()
            return redirect('users:login')  # Редирект на страницу входа
        except User.DoesNotExist:
            return HttpResponse('Неверная ссылка подтверждения.')


class ProfileView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    request.user.set_password(new_password)
    request.user.save()

    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('catalog_app:home'))
