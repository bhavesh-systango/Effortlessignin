import time
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def user_created_email_send(first_name, last_name, email, uid, token, protocol, domain):
    '''
        celery task to send email when the user is created

        -added the sleep time 10 second for testing if the task
        is working as expected
    '''

    time.sleep(10)
    send_mail(
        "Login credential for effortles ESS",  # subject
        f"\
        Hello, {first_name} {last_name}, your EffortLes ESS login credential are as followes: \n \
        email - {email} \n \
        set password using below link- \
        {protocol}://{ domain }/authentication/reset/{uid}/{token} \
        make sure to change the password after login into you account.",  # message
        "Effortles team",  # from
        [email],  # to
    )
