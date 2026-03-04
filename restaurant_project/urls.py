from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from menu import views as menu_views
from accounts import views as accounts_views
from orders import views as orders_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_views.index, name='index'),
    path('menu/', menu_views.public_menu, name='public_menu'),
    path('waiter/login/', accounts_views.waiter_login, name='waiter_login'),
    path('chef/login/', accounts_views.chef_login, name='chef_login'),
    path('waiter/hall/', accounts_views.waiter_hall, name='waiter_hall'),
    path('waiter/history/', accounts_views.waiter_history, name='waiter_history'),
    path('order/create/<int:table_id>/', orders_views.create_order, name='create_order'),
    path('order/<int:order_id>/', orders_views.order_detail, name='order_detail'),
    path('payment/<int:order_id>/', orders_views.payment, name='payment'),
    path('kitchen/', orders_views.kitchen_dashboard, name='kitchen_dashboard'),
    path('kitchen/update-item/<int:item_id>/', orders_views.update_order_item_status, name='update_order_item_status'),
    path('reports/', include('reports.urls')),
    path('booking/', include('booking.urls')),
    path('reservations/', include('booking.urls')),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
    path('', include('pwa.urls')),
]