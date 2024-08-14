from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)



class BankDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_no = models.IntegerField()
    ifsc_code = models.CharField(max_length=15)
    account_name = models.CharField(max_length=25)
    date_time = models.DateTimeField(auto_now=True)



class Platform_price(models.Model):
    UST_Price=models.DecimalField(max_digits=4, decimal_places=2)    
    Price1=models.DecimalField(max_digits=4, decimal_places=2)    
    Price2=models.DecimalField(max_digits=4, decimal_places=2)    
    Price3=models.DecimalField(max_digits=4, decimal_places=2)  

class Announcement(models.Model):
    Time=models.TimeField(auto_now=True)
    value_price=models.IntegerField()

class Exchange_price(models.Model):
    Average=models.DecimalField(max_digits=4, decimal_places=2)
    min_rate=models.DecimalField(max_digits=3, decimal_places=1)
    max_rate=models.DecimalField(max_digits=3, decimal_places=1)



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile number must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **extra_fields)

class User(AbstractBaseUser):
    mobile = models.CharField(max_length=15, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser 

class OTP(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Network(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name

class Address(models.Model):

    network = models.ForeignKey(Network, related_name='addresses', on_delete=models.CASCADE)
    deposit_address = models.CharField(max_length=200)

    def _str_(self):
        return f"{self.deposit_address} ({self.network.name})"
        
class Deposit(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    user = models.ForeignKey(User, related_name='deposits', on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    deposit_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Deposit of {self.deposit_amount} {self.network.name} by {self.user.mobile}"                