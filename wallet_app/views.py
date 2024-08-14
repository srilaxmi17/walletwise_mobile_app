from django.shortcuts import render
from rest_framework import generics,permissions
# from rest_framework.views import APIView
from wallet_app.models import *
from wallet_app.serializers import *
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from wallet_app.models import BankDetails
from rest_framework.permissions import IsAuthenticated
import string
from django.shortcuts import render, redirect, get_object_or_404
import re
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
import random
from django.contrib.auth import get_user_model
from wallet_app.models import OTP
from django.db.models import Sum
from wallet_app.serializers import OTPRequestSerializer


class BankDetailsManageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank_detail = serializer.save(user=request.user)  # Associate with the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        bank_detail = BankDetails.objects.get(user=request.user)
        serializer = self.get_serializer(bank_detail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BankDetailsUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankDetailsSerializer

    def get_object(self):
        """
        This method gets the bank details object based on the `id` provided
        and ensures it belongs to the authenticated user.
        """
        user = self.request.user
        bank_detail_id = self.kwargs.get('id')
        try:
            # Ensure the bank detail belongs to the authenticated user
            bank_detail = BankDetails.objects.get(id=bank_detail_id, user=user)
            return bank_detail
        except BankDetails.DoesNotExist:
            raise Http404("Bank details not found or not owned by the user")

    def put(self, request, *args, **kwargs):
        """
        Handle PUT request to update bank details.
        """
        bank_detail = self.get_object()
        serializer = self.get_serializer(bank_detail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)





class Platform_pricelist(generics.ListAPIView):
    permission_classes=[permissions.AllowAny]
    serializer_class=Platform_priceSerializers
    queryset=Platform_price.objects.all()

class announcementlist(generics.ListAPIView):
    permission_classes=[permissions.AllowAny]
    queryset=Announcement.objects.all()
    serializer_class=announcementSerializers    

class Exchange_pricelist(generics.ListAPIView):
    permission_classes=[permissions.AllowAny]
    queryset=Exchange_price.objects.all()
    serializer_class=ExchangePriceSerialziers


User = get_user_model()

# Initialize Twilio client with actual credentials
twilio_client = Client('AC3662be810b7aea8ab5bc0a495cc6d38b', '85e1be4c41faa0b44ece5a676dcb14dd')

otp_storage = {}

def send_otp(mobile):
    otp = random.randint(100000, 999999)
    otp_storage[mobile] = otp
    OTP.objects.create(phone=mobile, otp=otp)
    try:
        message = twilio_client.messages.create(
            body=f'Your OTP is {otp}',
            from_='+19383003259',
            to=mobile
        )
    except Exception as e:
        print(f"Twilio Error: {e}")
        raise e
    return message.sid

class LoginRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate mobile number format
        if not re.match(r'^\+\d{10,15}$', mobile):
            return Response({'error': 'Invalid mobile number format. Use the format: +1234567890'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(mobile=mobile)
            send_otp(mobile)
            return Response({'message': 'OTP sent to existing user'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            send_otp(mobile)
            return Response({'message': 'OTP sent for registration'}, status=status.HTTP_200_OK)

class VerifyOtpAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        if not mobile or not otp:
            return Response({'error': 'Mobile number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if otp_storage.get(mobile) == int(otp):
            user, created = User.objects.get_or_create(mobile=mobile)
            if created:
                user.set_password(User.objects.make_random_password())
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOtpAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

        send_otp(mobile)
        return Response({'message': 'OTP resent'}, status=status.HTTP_200_OK)

class OTPAutofillView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp_instance = OTP.objects.filter(phone=phone).order_by('-created_at').first()
            if otp_instance:
                return Response({'otp': otp_instance.otp}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No OTP found for this phone number'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ChooseNetworkAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        networks = Network.objects.all()
        return Response({'networks': [network.name for network in networks]})

class GetDepositAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        network_name = request.data.get('network')
        network = get_object_or_404(Network, name=network_name)
        addresses = Address.objects.filter(network=network)
        
        if not addresses.exists():
            return Response({'error': 'No deposit addresses available for the selected network.'}, status=status.HTTP_404_NOT_FOUND)
        
        deposit_address = random.choice(addresses).deposit_address
        request.session['selected_network'] = network_name
        request.session['deposit_address'] = deposit_address
        return Response({'deposit_address': deposit_address})



class EnterDepositAmountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        deposit_amount = request.data.get('deposit_amount')

        network_name = request.session.get('selected_network')
        deposit_address_value = request.session.get('deposit_address')

        if not network_name or not deposit_address_value:
            return Response({'error': 'Session data missing. Please select a network and get a deposit address first.'}, status=status.HTTP_400_BAD_REQUEST)

        network = get_object_or_404(Network, name=network_name)
        deposit_address = Address.objects.filter(deposit_address=deposit_address_value, network=network).first()

        if not deposit_address:
            return Response({'error': 'Address does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = self.generate_transaction_id()

        # Using a placeholder user ID or None
        user = request.user

        deposit = Deposit.objects.create(
            user= user,
            network=network,
            deposit_address=deposit_address,
            deposit_amount=deposit_amount,
            transaction_id=transaction_id
        )

        # Clear the session data after creating the deposit
        request.session.pop('selected_network', None)
        request.session.pop('deposit_address', None)

        response_data = {
            'network': network_name,
            'deposit_address': deposit_address_value,
            'deposit_amount': deposit_amount,
            'transaction_id': transaction_id,
            'created_time': deposit.created_time
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        latest_deposit = Deposit.objects.filter(user=user).order_by('-created_time').first()
        if not latest_deposit:
            return Response({'error': 'No deposits found'}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'deposit_amount': latest_deposit.deposit_amount,
            'deposit_address': latest_deposit.deposit_address.deposit_address,
            'network': latest_deposit.network.name,
            'transaction_id': latest_deposit.transaction_id,
            'created_time': latest_deposit.created_time
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def generate_transaction_id(self):
        return f"Tc{''.join(random.choices('0123456789', k=18))}"


    
class DepositHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        deposits = Deposit.objects.filter(user=user).order_by('-created_time')
        
        history = []
        for deposit in deposits:
            history.append({
                'network': deposit.network.name,
                'deposit_address': deposit.deposit_address.deposit_address,
                'created_time': deposit.created_time,
                'status': deposit.status,
                'deposit_amount': deposit.deposit_amount,
                'transaction_id': deposit.transaction_id,
            })
        
        return Response({'history': history}, status=status.HTTP_200_OK)    





class AvailableBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_balance = Deposit.objects.filter(user=user, status='completed').aggregate(total=Sum('deposit_amount'))['total'] or 0.00
        return Response({'available_balance': total_balance}, status=status.HTTP_200_OK)