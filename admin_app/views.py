from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from wallet_app.models import Admin,Platform_price,Exchange_price,Announcement,Network,Address,Deposit
from decimal import Decimal, InvalidOperation



def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return redirect('admin_app:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        new_admin = Admin(username=username)
        new_admin.set_password(password)
        
        try:
            new_admin.save()
            return redirect('admin_app:login')
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        admin = Admin.objects.filter(username=username).first()
        
        if admin and admin.check_password(password):
            request.session['admin_id'] = admin.id
            return redirect('admin_app:index')
        else:
            return render(request, 'login.html', {'error': 'Incorrect Username Or Password'})

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('admin_app:login')

@admin_required
def index(request):

    return render(request, 'index.html')

@admin_required
def add_platform_price_view(request):
    if request.method == 'POST':
        ust_price = request.POST.get('UST_Price')
        price1 = request.POST.get('Price1')
        price2 = request.POST.get('Price2')
        price3 = request.POST.get('Price3')

        try:
 
            ust_price = Decimal(ust_price)
            price1 = Decimal(price1)
            price2 = Decimal(price2)
            price3 = Decimal(price3)

            new_price = Platform_price(
                UST_Price=ust_price,
                Price1=price1,
                Price2=price2,
                Price3=price3
            )
            new_price.save()
            return redirect('admin_app:add_price') 

        except InvalidOperation:

            error_message = "Invalid input for prices. Please enter valid decimal numbers."
            return render(request, 'add_price.html', {'error': error_message})

        except Exception as e:

            return render(request, 'add_price.html', {'error': str(e)})
    return render(request, 'add_price.html')

@admin_required
def list_platform_prices_view(request):
    prices = Platform_price.objects.all()
    return render(request, 'list_prices.html', {'prices': prices})


@admin_required
def edit_platform_price_view(request, price_id):

    price = get_object_or_404(Platform_price, id=price_id)

    if request.method == 'POST':
        ust_price = request.POST.get('UST_Price')
        price1 = request.POST.get('Price1')
        price2 = request.POST.get('Price2')
        price3 = request.POST.get('Price3')

        try:

            ust_price = Decimal(ust_price)
            price1 = Decimal(price1)
            price2 = Decimal(price2)
            price3 = Decimal(price3)

            price.UST_Price = ust_price
            price.Price1 = price1
            price.Price2 = price2
            price.Price3 = price3
            price.save()

            return redirect('admin_app:list_platform_prices') 

        except InvalidOperation:
 
            error_message = "Invalid input for prices. Please enter valid decimal numbers."
            return render(request, 'edit_price.html', {'price': price, 'error': error_message})

        except Exception as e:

            error_message = f"An unexpected error occurred: {e}"
            return render(request, 'edit_price.html', {'price': price, 'error': error_message})

    return render(request, 'edit_price.html', {'price': price})


@admin_required
def delete_platform_price_view(request, price_id):
    price = get_object_or_404(Platform_price, id=price_id)
    
    if request.method == 'POST':
        price.delete()
        return redirect('admin_app:list_platform_prices') 
    return render(request, 'delete_price.html', {'price': price})

@admin_required
def add_exchange_price_view(request):
    if request.method == 'POST':
        average = request.POST.get('Average')
        min_rate = request.POST.get('min_rate')
        max_rate = request.POST.get('max_rate')

        try:
            average = Decimal(average)
            min_rate = Decimal(min_rate)
            max_rate = Decimal(max_rate)

            if min_rate > max_rate:
                raise ValueError('Minimum rate cannot be greater than maximum rate.')
            if not (min_rate <= average <= max_rate):
                raise ValueError('Average rate must be between minimum and maximum rate.')

            new_price = Exchange_price(
                Average=average,
                min_rate=min_rate,
                max_rate=max_rate
            )
            new_price.save()
            return redirect('admin_app:add_exchange_price')

        except (InvalidOperation, ValueError) as e:
            error_message = str(e)
            return render(request, 'add_exchange_price.html', {'error': error_message})

        except Exception as e:

            error_message = f"An unexpected error occurred: {e}"
            return render(request, 'add_exchange_price.html', {'error': error_message})

    return render(request, 'add_exchange_price.html')

@admin_required
def list_exchange_prices_view(request):
    prices = Exchange_price.objects.all()
    return render(request, 'list_exchange_prices.html', {'prices': prices})

@admin_required
def edit_exchange_price_view(request, price_id):
    price = get_object_or_404(Exchange_price, id=price_id)
    
    if request.method == 'POST':
        average = request.POST.get('Average')
        min_rate = request.POST.get('min_rate')
        max_rate = request.POST.get('max_rate')

        try:

            average = Decimal(average)
            min_rate = Decimal(min_rate)
            max_rate = Decimal(max_rate)

            if min_rate > max_rate:
                raise ValueError('Minimum rate cannot be greater than maximum rate.')
            if not (min_rate <= average <= max_rate):
                raise ValueError('Average rate must be between minimum and maximum rate.')

            price.Average = average
            price.min_rate = min_rate
            price.max_rate = max_rate
            price.save()
            return redirect('admin_app:list_exchange_prices') 

        except (InvalidOperation, ValueError) as e:

            error_message = str(e)
            return render(request, 'edit_exchange_price.html', {'price': price, 'error': error_message})

        except Exception as e:

            error_message = f"An unexpected error occurred: {e}"
            return render(request, 'edit_exchange_price.html', {'price': price, 'error': error_message})
    return render(request, 'edit_exchange_price.html', {'price': price})

@admin_required
def delete_exchange_price_view(request, price_id):
    price = get_object_or_404(Exchange_price, id=price_id)

    if request.method == 'POST':
        price.delete()
        return redirect('admin_app:list_exchange_prices') 
    return render(request, 'delete_exchange_price.html', {'price': price})

@admin_required
def add_announcement_view(request):
    if request.method == 'POST':
        value_price = request.POST.get('value_price')

        try:
            value_price = int(value_price)
            new_announcement = Announcement(value_price=value_price)
            new_announcement.save()
            return redirect('admin_app:add_announcement') 

        except ValueError:
            error_message = "Invalid input for value price. Please enter a valid integer."
            return render(request, 'add_announcement.html', {'error': error_message})
    return render(request, 'add_announcement.html')

@admin_required
def list_announcements_view(request):
    announcements = Announcement.objects.all()
    return render(request, 'list_announcements.html', {'announcements': announcements})


@admin_required
def edit_announcement_view(request, announcement_id):

    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == 'POST':
        value_price = request.POST.get('value_price')

        try:
            value_price = int(value_price)
            announcement.value_price = value_price
            announcement.save()
            return redirect('admin_app:list_announcements') 

        except ValueError:

            error_message = "Invalid input for value price. Please enter a valid integer."
            return render(request, 'edit_announcement.html', {'announcement': announcement, 'error': error_message})
    return render(request, 'edit_announcement.html', {'announcement': announcement})


@admin_required
def delete_announcement_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == 'POST':
        announcement.delete()
        return redirect('admin_app:list_announcements')
    return render(request, 'delete_announcement.html', {'announcement': announcement})

@admin_required
def add_network_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        try:
            if not name:
                raise ValueError("Network name cannot be empty.")
            new_network = Network(name=name)
            new_network.save()
            return redirect('admin_app:add_network')

        except ValueError as e:
            error_message = str(e)
            return render(request, 'add_network.html', {'error': error_message})
    return render(request, 'add_network.html')


@admin_required
def list_networks_view(request):
    networks = Network.objects.all()
    return render(request, 'list_networks.html', {'networks': networks})



@admin_required
def edit_network_view(request, network_id):
    network = get_object_or_404(Network, id=network_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')

        try:
            if not name:
                raise ValueError("Network name cannot be empty.")

            network.name = name
            network.save()
            return redirect('admin_app:list_networks') 

        except ValueError as e:
            error_message = str(e)
            return render(request, 'edit_network.html', {'network': network, 'error': error_message})

    return render(request, 'edit_network.html', {'network': network})


@admin_required
def add_address_view(request):
    if request.method == 'POST':
        network_id = request.POST.get('network')
        deposit_address = request.POST.get('deposit_address')

        try:
            network = get_object_or_404(Network, id=network_id)
            new_address = Address(network=network, deposit_address=deposit_address)
            new_address.save()
            return redirect('admin_app:add_address')
        except Exception as e:
            return render(request, 'add_address.html', {'error': str(e), 'networks': Network.objects.all()})
    
    return render(request, 'add_address.html', {'networks': Network.objects.all()})


@admin_required
def list_addresses_view(request):
    addresses = Address.objects.all()
    return render(request, 'list_addresses.html', {'addresses': addresses})


@admin_required
def edit_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    
    if request.method == 'POST':
        network_id = request.POST.get('network')
        deposit_address = request.POST.get('deposit_address')

        try:
            network = get_object_or_404(Network, id=network_id)
            address.network = network
            address.deposit_address = deposit_address
            address.save()
            return redirect('admin_app:list_addresses')
        except Exception as e:
            return render(request, 'edit_address.html', {'address': address, 'networks': Network.objects.all(), 'error': str(e)})
    
    return render(request, 'edit_address.html', {'address': address, 'networks': Network.objects.all()})


@admin_required
def delete_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        address.delete()
        return redirect('admin_app:list_addresses')
    return render(request, 'delete_address.html', {'address': address})
    
    
    
@admin_required
def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    if deposit.status != 'completed':
        deposit.status = 'completed'
        deposit.save()
        messages.success(request, f'Deposit {deposit.transaction_id} has been approved.')
    else:
        messages.info(request, f'Deposit {deposit.transaction_id} is already approved.')
    return redirect('admin_app:list_deposits')

@admin_required
def reject_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    if deposit.status != 'failed':
        deposit.status = 'failed'
        deposit.save()
        messages.error(request, f'Deposit {deposit.transaction_id} has been rejected.')
    else:
        messages.info(request, f'Deposit {deposit.transaction_id} is already rejected.')
    return redirect('admin_app:list_deposits')



@admin_required
def list_deposits(request):
    deposits = Deposit.objects.all()
    return render(request, 'list_deposits.html', {'deposits': deposits})