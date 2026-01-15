from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# @receiver = Decorator that registers this function as signal handler
@receiver(post_save, sender=User)
# post_save = Signal sent AFTER saving an object
# sender=User = Only listen for User saves
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:  # created=True only when NEW user is created
        Profile.objects.create(user=instance)
        # Automatically create a Profile for the new user

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    instance.profile.save()
    # When user is saved, also save their profile
