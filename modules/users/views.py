from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm

User = get_user_model()


class SignupView(CreateView):
    """Страница регистрации нового пользователя."""

    form_class = CreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
