from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages

from .models import CustomUser
from .forms import RegistrationForm, UserEditForm
from .tokens import account_activation_token


@login_required
def dashboard(request):
    
    return render(request, 'accounts/dashboard.html')


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/user/edit_details.html', {'user_form': user_form})


def account_register(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.username = registerForm.cleaned_data['user_name']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'activate your account'
            message = render_to_string('accounts/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/registration/email_verification_sent.html')
    else:
        registerForm = RegistrationForm()
    return render(request, 'accounts/registration/registration.html', {'form': registerForm})






def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')

# DELETE USER


@login_required
def delete_user(request):
    user = CustomUser.objects.get(user_name=request.user)
    # we are inactivating the user instead of deleting the whole user
    user.is_active = False
    user.save()
    logout(request)
    return redirect('users:delete_confirmation')
