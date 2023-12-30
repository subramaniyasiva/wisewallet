# wisewallet/urls.py

from django.contrib import admin
from django.urls import path, include
from wisewallet.views import expense_list, home, about, contact_us, signup, signin, save_expense_data,get_expense_details,delete_expense,update_expense,get_old_entries

app_name = 'wisewallet'  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('about/', about, name='about'),
    path('expenses/', expense_list, name='expense_list'),
    path('signup/', signup, name='signup'),
    path('save_expense_data/', save_expense_data, name='save_expense_data'),
    path('contact_us/', contact_us, name='contact_us'),
    path('signin/', signin, name='signin'),
    path('get_expense_details/', get_expense_details, name='get_expense_details'),
    path('delete_expense/', delete_expense, name='delete_expense'),
    path('update_expense/', update_expense, name='update_expense'),
    path('get_old_entries/', get_old_entries, name='get_old_entries'),
]
