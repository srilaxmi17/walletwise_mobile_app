# admin.py
from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'is_staff', 'is_superuser')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'created_at')

# admin.site.register(Platform_price)
# admin.site.register(Announcement)
# admin.site.register(Exchange_price)
