from django.db import models
from django.contrib.auth.hashers import make_password ,check_password

# Create your models here.
class Registerd_user(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super(Registerd_user, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class User(models.Model):
    user= models.OneToOneField(Registerd_user, on_delete= models.CASCADE , related_name= 'user_profile')
    #full_name = models.CharField(max_length= 20 , blank= False )
    email = models.EmailField(max_length=50 , default= 'Update_your_email@gmail.com')
    total_budget = models.DecimalField( max_digits= 10 , decimal_places= 2 , default= 0)
    budget_remaining = models.DecimalField( max_digits= 10 , decimal_places= 2 , default =0)
    
    def __str__(self):
        return self.user.username
class Expenses(models.Model):
    user= models.ForeignKey(Registerd_user,on_delete= models.CASCADE , related_name= 'expenses') 
    date = models.DateField()
    amount = models.DecimalField(max_digits= 10 , decimal_places= 2 , default =0)
    category = models.CharField(max_length=20 , choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Others', 'Others'),
    ])
    description = models.TextField(blank= True)
    def __str__ (self) :
        return f"{self.user.username} - {self.category} -${self.amount}" 


