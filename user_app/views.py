from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, UserForm
from .models import User
from django.contrib.auth.decorators import login_required


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            return render(request, 'user_app/login_user.html', {'login_fail': "Benutzer nicht gefunden"})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user_app/login_user.html', {'login_fail': "Passwort oder Benutzer falsch."})

    return render(request, 'user_app/login_user.html', {'login_fail': None})


def registerPage(request):
    form = CustomUserCreationForm()
    error_registration = None

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            error_registration = "Fehler bei der Registrierung"

    return render(request, 'user_app/register_user.html', {'form': form, "error_registration": error_registration})


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='user-login-required')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-account', pk=user.id)

    return render(request, 'user_app/update_user.html', {'form': form})

@login_required(login_url='user-login-required')
def userAccount(request):
    user = request.user
    context = {"user": user}
    return render(request, 'user_app/account_user.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    recipes = user.recipe_set.all()
    context = {'user': user, "recipes": recipes}
    return render(request, 'user_app/profile_user.html', context)


def loginRequired(request):
    return render(request, 'user_app/login_required.html')