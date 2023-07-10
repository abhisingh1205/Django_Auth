from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from .models import User
from django.dispatch import receiver
from .utils import Util

@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    body = 'Successfully logged in!'
    data = {
        'subject' : 'Successfull Login',
        'body': body,
        'to_email': user.email
    }

    #Util.send_email(data)

@receiver(post_save, sender=User, dispatch_uid='Send Message')
def send_message_signal(sender, instance, **kwargs):
    print("send_message_signal signal called")


@receiver(pre_save, sender=User)
def at_beginning_save(sender, instance, **kwargs):
    print("-------------")
    print("Inside at_beginning_save")
    print("Sender = ", sender)
    print("Instance = ", instance)
    print(f"Kwargs {kwargs}")


@receiver(post_save, sender=User)
def at_ending_save(sender, instance, created, **kwargs):
    if created:
        print("POST SAVE SIGNAL-------------")
        print("New Record")
        print("Sender = ", sender)
        print("Instance = ", instance)
        print("Created = ", created)
        print(f"Kwargs {kwargs}")
    else:
        print("POST SAVE SIGNAL-------------")
        print("Update")
        print("Sender = ", sender)
        print("Instance = ", instance)
        print("Created = ", created)
        print(f"Kwargs {kwargs}")


@receiver(pre_delete, sender=User)
def at_beginning_delete(sender, instance, **kwargs):
    print("-------------")
    print("Inside at_beginning_delete")
    print("Sender = ", sender)
    print("Instance = ", instance)
    print(f"Kwargs {kwargs}")

@receiver(post_delete, sender=User)
def at_ending_delete(sender, instance, **kwargs):
    print("-------------")
    print("Inside at_ending_delete")
    print("Sender = ", sender)
    print("Instance = ", instance)
    print(f"Kwargs {kwargs}")

