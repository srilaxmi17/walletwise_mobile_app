from django.urls import path
from admin_app import views

app_name = 'admin_app'


urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_price/', views.add_platform_price_view, name='add_price'),
    path('view_prices/', views.list_platform_prices_view, name='list_platform_prices'),
    path('edit_price/<int:price_id>/', views.edit_platform_price_view, name='edit_platform_price'),
    path('delete_price/<int:price_id>/', views.delete_platform_price_view, name='delete_platform_price'),
    path('add_exchange_price/', views.add_exchange_price_view, name='add_exchange_price'),
    path('list_exchange_prices/', views.list_exchange_prices_view, name='list_exchange_prices'),
    path('edit_exchange_price/<int:price_id>/', views.edit_exchange_price_view, name='edit_exchange_price'),
    path('delete_exchange_price/<int:price_id>/', views.delete_exchange_price_view, name='delete_exchange_price'),
    path('add_announcement/', views.add_announcement_view, name='add_announcement'),
    path('list_announcements/', views.list_announcements_view, name='list_announcements'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement_view, name='edit_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement_view, name='delete_announcement'),
    path('add_network/', views.add_network_view, name='add_network'),
    path('list_networks/', views.list_networks_view, name='list_networks'),
    path('edit_network/<int:network_id>/', views.edit_network_view, name='edit_network'),

    path('add_address/', views.add_address_view, name='add_address'),
    path('list_addresses/', views.list_addresses_view, name='list_addresses'),
    path('edit_address/<int:address_id>/', views.edit_address_view, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address_view, name='delete_address'),
    
    path('approve_deposit/<int:deposit_id>/', views.approve_deposit, name='approve_deposit'),
    path('reject_deposit/<int:deposit_id>/', views.reject_deposit, name='reject_deposit'),
    path('deposits/', views.list_deposits, name='list_deposits'),

]