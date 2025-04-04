from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registerd_user, User , Expenses
from datetime import date

@receiver(post_save, sender=Registerd_user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       User.objects.create(
            user=instance,
            email="Update_your_email@gmail.com",
            total_budget=0.0,
            budget_remaining=0.0
        )
       Expenses.objects.create(
            user=instance,
            date=date.today(),  # Or use `date.today()` if required
            amount=0.0,
            category='Others',
            description='Initial expense placeholder'
        )
       
