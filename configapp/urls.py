from django.urls import path, include
from configapp.views import *

urlpatterns = [
    path('', index, name='home'),
    path('login', login_page, name='login'),
    path('login/admin_panel/', admin_panel, name='admin_panel'),
    path('login/staff/', staff_panel, name='staff_panel'),
    path('add_user/', add_user, name='add_user'),
    path('blog/', blog, name='blog'),
    path('blog-details/', blog_details, name='blog-details'),
    path('contact/', contact_view, name='contact'),
    path('messages/', messages_view, name='messages'),
]
