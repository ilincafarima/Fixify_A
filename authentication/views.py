from django.shortcuts import render, redirect
from .forms import RegistrationForm, SearchForm
from django.shortcuts import redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from blog.models import BlogPost  # Import the BlogPost mode
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  # Redirect to home page after successful login
        else:
            # Check if the username exists in the database
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Invalid password. Please try again.')
            else:
                messages.error(request, 'User does not exist. Please register.')
    
    return render(request, 'login.html')

def landing_page(request):
    # Fetch the last three blog posts
    last_three_posts = BlogPost.objects.order_by('-timestamp')[:3]

    # Pass the last three blog posts to the template context
    return render(request, 'home.html', {'last_three_posts': last_three_posts})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def search_view(request):
    query = request.GET.get('query', '').strip()  # Get the query parameter from the request

    if query:  # Check if the query parameter is not empty
        # Search across multiple fields using Q objects
        results = CustomUser.objects.filter(
            Q(role='Fixer') & 
            (Q(username__icontains=query) |  # Search in username field
             Q(email__icontains=query) |     # Search in email field
             Q(first_name__icontains=query) |  # Search in first name field
             Q(last_name__icontains=query)   # Search in last name field
             # Add more fields as needed
            )
        )
        print("Search query:", query)  # Print the search query for debugging
        print("Search results:", results)  # Print search results for debugging

        return render(request, 'search_results.html', {'results': results, 'query': query})

    # If no query parameter or invalid query, return an empty result or error message
    return render(request, 'search_results.html', {'results': [], 'query': ''})

@login_required
def profile_view(request):
    # Assuming you have a template named 'profile.html' to render the user's profile
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout
    return redirect('landing_page')  # Redirect to the landing page after logout