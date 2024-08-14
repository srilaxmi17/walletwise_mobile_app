from rest_framework import serializers
from wallet_app.models import *

class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ['id', 'account_no', 'ifsc_code', 'account_name', 'date_time']

class Platform_priceSerializers(serializers.ModelSerializer):
    class Meta:
        model=Platform_price
        fields='__all__'

class announcementSerializers(serializers.ModelSerializer):
    class Meta:
        model= Announcement
        fields='__all__'

class ExchangePriceSerialziers(serializers.ModelSerializer):
    class Meta:
        model=Exchange_price
        fields='__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'network', 'deposit_address', 'created_time', 'deposit_amount', 'transaction_id', 'status']

class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
