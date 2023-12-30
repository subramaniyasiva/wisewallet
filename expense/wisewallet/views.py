from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExpenseForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from expense.models import WExpense
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_http_methods
import json
from .models import Expense

from django.http import JsonResponse

def get_old_entries(request):
    try:
        old_entries = Expense.objects.all()
        total_old_entries = old_entries.aggregate(sum('value'))['value__sum'] or 0

        old_entries_list = [
            {'date': entry.date.strftime('%Y-%m-%d'), 'label': entry.label, 'value': entry.value}
            for entry in old_entries
        ]

        response_data = {'old_entries': old_entries_list, 'total_old_entries': total_old_entries}
        return JsonResponse(response_data)
    except Exception as e:
        # Log the exception for debugging
        print(f"Exception in get_old_entries: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@csrf_exempt
def delete_expense(request):
    if request.method == 'DELETE':
        expense_id = request.GET.get('id')

        try:
            # Assuming you have a model named Expense
            expense = Expense.objects.get(pk=expense_id)

            # Check if the user is the owner of the expense
            if expense.user != request.user:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

            # Delete the expense
            expense.delete()

            return JsonResponse({'status': 'success'})
        except Expense.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Expense not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@require_POST
def update_expense(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        expense_id = data.get('id')
        date = data.get('date')
        label = data.get('label')
        value = data.get('value')

        # Fetch and update the expense
        expense = Expense.objects.get(pk=expense_id)
        expense.date = date
        expense.label = label
        expense.value = value
        expense.save()

        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    except Expense.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Expense not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def save_expense_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            expense_entries = data.get('data', [])

         
            expense_objects = [
                Expense(
                    user=request.user,
                    date=entry.get('date'),
                    label=entry.get('label'),
                    value=entry.get('value')
                )
                for entry in expense_entries
            ]

            Expense.objects.bulk_create(expense_objects)

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def save_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            print(form.errors)
            
            print(f'Date: {form.cleaned_data["date"]}')
            print(f'Label: {form.cleaned_data["label"]}')
            print(f'Value: {form.cleaned_data["value"]}')
      
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
         

            return redirect(reverse('expense_list'))
            


    else:
        
        form = ExpenseForm()

    return render(request, 'exp.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return redirect('expense_list')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})



@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'exp.html', {'expenses': expenses})




def home(request):
   
    context = {
        'page_title': 'Welcome to wisewallet 📈',
        'dynamic_data': 'Some dynamic data for demonstration',  
    }
    return render(request, 'E:/django project/expense/templates/home.html', context)
def about(request):
    return render(request, 'E:/django project/expense/templates/about.html')
def contact_us(request):
    return render(request,'E:/django project/expense/templates/contact us.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
        else:
             print(form.errors) 
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
def get_expense_details(request):
    expense_id = request.GET.get('id')

    try:
        
        expense = Expense.objects.get(pk=expense_id)

        
        expense_details = {
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'label': expense.label,
            'value': expense.value,
        }

        return JsonResponse(expense_details)
    except Expense.DoesNotExist:
        return JsonResponse({'error': 'Expense not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
