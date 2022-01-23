# Note that you'll want to ensure you place this code snippet in an installed models.py module, or some other location
# that will be imported by Django on startup.


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        # here we are auto generating token for each single user

