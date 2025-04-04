from django.shortcuts import render , redirect
from django.http import HttpResponse , response 
from .models import  *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login 
from django.db.models import Sum
import json
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def welcome( request ):
    print("Session Data:", request.session.items())
    session_user = request.session.get('username')
    registered_user = Registerd_user.objects.get(username=session_user )
     # Access User model details using the related_name 'User'
    user_details = Registerd_user.objects.select_related('user_profile').get(username=session_user)
    print( user_details , type(user_details) , user_details.username)
    
    if hasattr(user_details, 'user_profile'):
            context = {
                'username': user_details.username,
                'email': user_details.user_profile.email,
                'total_budget': user_details.user_profile.total_budget,
                'budget_remaining': user_details.user_profile.budget_remaining,
            }
    else:
        context={
        'username': user_details.username ,
        'email': 'updatemail@gmail.com',
        'total_budget': 0,
        'budget_remaining': 0
    }
    #user= User.objects.create ( username = 'Audrey' , full_name = ' Ok Audrey' , email = 'asdfdgfh@gmail.com' , total_budget = 200 , budget_remaining= 300)
    return render( request , 'expenses/welcome.html' ,{ 'user' : context})

def edit_summary(request):
    if request.method == 'POST' :
        email_val= request.POST.get('email')
        add_val= request.POST.get('add_amount')
        session_user = request.session.get('username')
        try:
            #user_details = Registerd_user.objects.select_related('user_profile').get(username=session_user)
            user_details = Registerd_user.objects.get(username=session_user)
            
            user_profile = user_details.user_profile  # Access the OneToOneField related object
            user_expn_profile = user_details.expenses.aggregate(total_amount=Sum('amount'))
            total_expenses = user_expn_profile['total_amount'] or 0
            # Update fields
            user_profile.email = email_val
            user_profile.total_budget = float(user_profile.total_budget)+ float (add_val)
            user_profile.budget_remaining = user_profile.total_budget - float(total_expenses)
            user_profile.save()

            return redirect('welcome')  # Redirect to dashboard or any success page
        except  :
            return render(request, 'expenses/error.html', {'error': 'Incorrect data to cannot be added '})
    return render(request, 'expenses/welcome.html')

def  home( request) :
    session_user = request.session.get('username')
    user_details = Registerd_user.objects.get(username=session_user)
    user_profile_dtl= user_details.user_profile
    user_expn_profile = user_details.expenses.aggregate(total_amount=Sum('amount'))
    total_expenses = user_expn_profile['total_amount'] or 0
    
    amount_summary =  { 'total_expenses' :  total_expenses , 'budget_remaining' : user_profile_dtl.budget_remaining
                        }
    expens= user_details.expenses.all().order_by('-date')
    if(total_expenses ==0 ) : expens={}
    return render(request , 'expenses/home.html' , { 'amount': amount_summary , 'expenses' : expens})

def add_expense(request):
    
    if request.method == 'POST' :
        date= request.POST.get('date')
        amount= request.POST.get('amount')
        category= request.POST.get('category')
        description= request.POST.get('description')
        session_user = request.session.get('username')
        user_details = Registerd_user.objects.get(username=session_user)
        Expenses.objects.create (user= user_details , date=date , amount= amount ,category= category, description = description )
        #expenses = Expenses.objects.all()
        Expenses.objects.filter(user=user_details, amount=0).delete()
        expenses = Expenses.objects.filter(user=user_details).order_by('-date')
        user_profile_dtl= user_details.user_profile
        user_expn_profile = user_details.expenses.aggregate(total_amount=Sum('amount'))
        total_expenses = user_expn_profile['total_amount'] or 0
        user_profile_dtl.budget_remaining = float(user_profile_dtl.total_budget) - float(total_expenses)
        user_profile_dtl.save()
        amount_summary =  { 'total_expenses' :  total_expenses , 'budget_remaining' : user_profile_dtl.budget_remaining
                        }
        
        return render(request, 'expenses/home.html' , {  'amount': amount_summary  , 'expenses' : expenses })
    else:
        return render(request, 'expenses/home.html')
    
def view_expenses(request):
    session_user = request.session.get('username')
    user_details = Registerd_user.objects.get( username = session_user )
    expenses = Expenses.objects.filter(user= user_details ).order_by('-date')
    user_profile_dtl= user_details.user_profile
    user_expn_profile = user_details.expenses.aggregate(total_amount=Sum('amount'))
    total_expenses = user_expn_profile['total_amount'] or 0
    user_profile_dtl.budget_remaining = float(user_profile_dtl.total_budget) - float(total_expenses)
    user_profile_dtl.save()
    amount_summary =  { 'total_expenses' :  total_expenses , 'budget_remaining' : user_profile_dtl.budget_remaining
    }
    current_year = datetime.now().year
    expenses = Expenses.objects.filter(user= user_details , date__year=current_year)
    monthly_expenses = (
            expenses
            .values('date__month')
            .annotate(total=Sum('amount'))
            .order_by('date__month')
        )
    all_months = {i: 0 for i in range(1, 13)}  # Dictionary with default value 0 for each month
    for entry in monthly_expenses:
        all_months[entry['date__month']] = float(entry['total'])  # Convert Decimal to float

    # Convert month numbers to readable labels
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    monthly_labels = month_names  
    monthly_data = list(all_months.values()) 
    if(total_expenses ==0 ) : expenses={}
    context = {
            'amount': amount_summary ,
            'expenses': expenses,
            'monthly_labels': json.dumps(monthly_labels),
            'monthly_data': json.dumps(monthly_data)
        }
    return render(request, 'expenses/view_expenses.html' ,context )

def user_register( request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            if Registerd_user.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                #hashed_password = make_password(password) as we are storing while loading to models we no need to hash here 
                Registerd_user.objects.create(username=username, password=password)
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'expenses/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Registerd_user.objects.get(username=username)

            # Correct password check
            if check_password(password, user.password):
                request.session['username'] = username
                messages.success(request, 'Login successful!')
                return redirect('welcome')
            else:
                messages.error(request, 'Invalid username or password.')
        except Registerd_user.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'expenses/login.html')



def user_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('login')
def test_session(request):
    request.session['username'] = 'TestUser'
    return HttpResponse(f"Session username set to: {request.session.get('username')}")

def change_password(request):
    if request.method == "POST":
        username = request.session.get('username')
        user = Registerd_user.objects.get(username=username)
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
    
        if not check_password(old_password, user.password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.password = new_password
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Password changed successfully!")
            return redirect("settings")
    session_user = request.session.get('username')
     # Access User model details using the related_name 'User'
    user_details = Registerd_user.objects.select_related('user_profile').get(username=session_user)
    user  = {
                'username': user_details.username }
    print( user)
    return render(request, "expenses/setting.html" , user )