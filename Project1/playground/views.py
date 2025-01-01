from django.shortcuts import render
from django.core.mail import send_mail, mail_admins , BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage


# Create your views here.

def hello(request):
    try:
        # send_mail('test mail', 'hello from me', 'info@domain.com', ['bob@moshy.com'])
        # message = EmailMessage('test mail', 'hello from me', from_email='test@mail.com', to=['annu@microsoft.com'])
        # message.attach_file('playground/static/images/doh.png')
        # message.send()
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'annu'}
        )
        message.send(['fake@mail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Anna'})