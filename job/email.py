from django.core.mail import BadHeaderError, send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


def jobmail(form):
    # Generate token and encode user primary key
    if form.application_link:
        apply_link = form.application_link
    else:
        apply_link = form.application_email
    # Send the email
    subject = "Job Alert"
    url = f"http://eduvjobs.herokuapp.com/jobs/activate?title={form.title}&recuiter={form.posted_by.pk}"
    url_1 = f"{apply_link}"
    url_2 = f"http://eduvjobs.herokuapp.com/jobs/delete?title={form.title}&recuiter={form.posted_by.pk}"
    html_message = f"""<div style="margin: 5% 0%;">

            <h2>New Job Posted</h2>
            Hello admin,<br><br>
                Recuiter: {form.posted_by}<br><br>
                Job Title: {form.title}<br><br>
                Date Posted: {form.date_created}<br><br>
                <a href=\"{url}\" style="color:white; text-decoration: none;border-radius: 25px; background-color: #754C28; padding: 7px 25px;"> <strong>Clear Job<strong></a><br><br>
                <br><a href=\"{url_1}\" style="color:white; text-decoration: none;border-radius: 25px; background-color: #754C28; padding: 7px 25px;"> <strong>Check Job<strong></a><br><br>
                <br><a href=\"{url_2}\" style="color:white; text-decoration: none;border-radius: 25px; background-color: #754C28; padding: 7px 25px;"> <strong>Delete Job<strong></a>
            </div>"""

    email_content = ""
    try:
        send_mail(subject, email_content, "helpraisemyfund@gmail.com",
                  ["helpraisemyfund@gmail.com"], fail_silently=False, html_message=html_message)
        return 'email sent successfully'
    except BadHeaderError:
        return 'email not sent'
