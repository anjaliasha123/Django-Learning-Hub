from django.shortcuts import render
import requests
import logging
# from django.utils.decorators import method_decorator
from rest_framework.views import APIView
# from django.views.decorators.cache import cache_page
# from .tasks import notify_customers
# from django.core.cache import cache
# from django.core.mail import send_mail, mail_admins , BadHeaderError, EmailMessage
# from templated_mail.mail import BaseEmailMessage

logger = logging.getLogger(__name__)

class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            response = requests.get('https://httpbin.org/delay/2')
            data = response.json()
            return render(request, 'hello.html', {'name': data})
        except requests.ConnectionError:
            logger.critical('httpbin is offline')

# Create your views here.
# @cache_page(5*60)
# def hello(request):
#     key = 'httpbin_result'
    # try:
        # send_mail('test mail', 'hello from me', 'info@domain.com', ['bob@moshy.com'])
        # message = EmailMessage('test mail', 'hello from me', from_email='test@mail.com', to=['annu@microsoft.com'])
        # message.attach_file('playground/static/images/doh.png')
        # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'annu'}
    #     )
    #     message.send(['fake@mail.com'])
    # except BadHeaderError:
    #     pass
    # notify_customers.delay('Hello')
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)
    # using caching views using decorator
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()
    # # return render(request, 'hello.html', {'name': cache.get(key)})
    # return render(request, 'hello.html', {'name': data})