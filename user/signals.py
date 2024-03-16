from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAccount, Profile

@receiver(post_save, sender=UserAccount)
def create_profile(sender, instance, created, **kwargs):
    
    if created:
        Profile.objects.create(user=instance)
        print("Profile created")
    
# post_save.connect(create_profile, sender=UserAccount)    

@receiver(post_save, sender=UserAccount)
def update_profile(sender, instance, created, **kwargs):
    
    if created == False:
        instance.profile.save()
        print("Profile Updated!")
        
# post_save.connect(update_profile, sender=UserAccount)    
# ctrl + shift + l = select dublicates