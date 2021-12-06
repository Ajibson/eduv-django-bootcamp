
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect
from .models import confirmation_email
from django.db import IntegrityError


def account_confirmation_email(request, instance):
    uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)
    subject = "Account Cofirmation"
    email_content = 'Here is the message.'
    url = f"http://localhost:8000/confirm-email/{uidb64}/{token}"
    html_message = f"""
                        <div>
                            <a href="{url}"></a>
                        </div>

                    """
    # Save the token
    try:
        confirmation_email.objects.create(user=instance, token=token)
    except IntegrityError:
        messages.success(request, 'An email has been sent!!!')
        return redirect("account:token")
    email_response = send_mail(subject, message=email_content, from_email='azeezaremu123@gmail.com',
                               recipient_list=[instance.email], fail_silently=False, html_message=html_message)
