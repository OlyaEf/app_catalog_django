from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, UpdateView
from django.shortcuts import redirect
from django.contrib import messages

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка письма для верификации
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите ваш аккаунт'
        message = render_to_string(
            'users/verify_email.html',
            {
                'user': self.object,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
                'token': default_token_generator.make_token(self.object),
            },
        )
        send_mail(mail_subject, message, 'noreply@localhost', [self.object.email])
        messages.success(self.request, 'Письмо с подтверждением отправлено на вашу почту.')
        return response


class VerifyEmailSentView(TemplateView):
    template_name = 'users/verify_email.html'
    success_url = reverse_lazy('users:profile')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
