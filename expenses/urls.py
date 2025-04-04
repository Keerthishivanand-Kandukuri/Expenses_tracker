from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home ) ,
    path('welcome/', welcome ,name='welcome' ) ,
    path('add_expense/', add_expense , name = 'add_expense' ) ,
    path('view-expenses/', view_expenses , name = 'view-expenses' ) ,
    path('register/', user_register , name='register') ,
    path('', user_login, name='login'),
    path('test_session/', test_session, name='test'),
    path('edit_summary/',edit_summary ,name = 'sum_edit'),
    path('settings/',change_password ,name = 'settings') , 
    path('logout/',user_logout ,name = 'logout') 
    
]