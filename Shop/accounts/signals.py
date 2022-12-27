from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from customers.models import Customer


@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])
