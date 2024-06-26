from django.shortcuts import render
from django.views.generic import CreateView
from .models import Contact
from django.urls import reverse_lazy
from .forms import ContactForm
from django.core.mail import send_mail

# send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['sandra.005@mail.ru'])

class ContactCreate(CreateView):
    model = Contact
    # fields = ["first_name", "last_name", "message"]
    success_url = reverse_lazy('success_page')
    form_class = ContactForm

    def form_valid(self, form):
        # Формируем сообщение для отправки
        data = form.data
        subject = f'Сообщение c JL от {data["name"]}  Почта отправителя: {data["email"]}'
        email(subject, data['message'])
        return super().form_valid(form)


# Функция отправки сообщения
def email(subject, content):
   send_mail(subject,
      content,
      'sandra.005@mail.ru',
      ['sandra.005@mail.ru']
   )

# Функция, которая вернет сообщение в случае успешного заполнения формы
def success(request):
   return render(request, 'contact_form/contact_answer.html')
