from datetime import timezone

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
#from django.views.generic import CreateView, FormView
from django.utils.http import is_safe_url
#from py2exe.boot_service import password
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, LoginForm, GuestForm, UserForm
from .models import GuestEmail, Profile


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'accounts/register.html'
#     success_url = '/login/'

# def base_template(request):
#     #now = datetime.datetime.now()
#     #now = request.user.update
#     #context = {"user": request.user}
#
#     return render(request, 'accounts_1/base_home_accounts_1.html')




def home(request):
    return render(request, 'accounts_1/index.html')



def guset_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")

@csrf_protect
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        #user.active = False
        if user is not None:
            # Is the account active? It could have been disabled.
            # user.is_active = False
            if user.is_active:
                login(request, user)
                return render(request, 'accounts_2/index.html')
                #return HttpResponseRedirect("/profile/")
            else:
                return HttpResponse("You have to Wait for admin approval.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'pass_admin_approval_wrong.html')
    else:
        return render(request, 'login.html', context)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {"form": form}
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         #password = form.cleaned_data.get("password")
#         username = authenticate(request, username=username)
#         #user.active = False
#         if username:
#             login(request, username)
#             UserAuthentified = True
#             return render(request, 'accounts/profile.html')
#         else:
#             print("Invalid login details: {0}".format(username))
#             return render(request, 'accounts/pass_admin_approval_wrong.html')
#     else:
#         return render(request, 'accounts/login.html', context)




User = get_user_model()
@csrf_protect
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return render(request, 'register_success.html')
    return render(request, 'register.html', context)


@login_required
def profile(request):
    #if request.user.update:
        #request.user.save()
    args = {"user": request.user }

    return render(request, 'accounts_2/index.html', args)


# @login_required
# def sub_profile(request):
#     return render(request, 'accounts/index.html')


@login_required
def charts(request):
    users = User.history.all()
    #args = {"user": request.user}
    users_2 = request.user.history.all()
    context = {
        "users": users,
        "users_2": users_2,
        "user": request.user
    }

    return render(request, 'accounts_2/dashboard_charts.html', context)



@login_required
def info(request):

    args = {
        "user": request.user,
        #"profile_user": request.user_
    }
    return render(request, 'accounts_2/info.html', args)



@login_required
def lead_number(request):
    # form = LoginForm()
    # username = form.username
    # password = form.password
    # user = authenticate(request, username=username, password=password)
    # context = {
    #     'lead': user.lead
    # }
    args = {
        "user": request.user,
        "profile_user": request.user_profile
    }
    return render(request, 'lead.html', args)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def contact_us(request):
    return render(request, 'contact_us.html')

def about(request):
    return render(request, 'about.html')


def coming_soon(request):
    return render(request, 'coming_soon.html')

def coming_soon_profile(request):
    return render(request, 'accounts_2/coming_soon_profile.html')

@login_required
def all_tasks(request):
    users = User.history.all()
    # args = {"user": request.user}
    context = {"users": users}
    return render(request, 'accounts_2/all_tasks.html', context)





