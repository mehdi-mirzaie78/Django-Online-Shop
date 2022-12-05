from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
from .utils import random_code, send_otp_code
from .models import OtpCode, User
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'core/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rand_code = random_code()
            send_otp_code(cd['phone'], rand_code)
            OtpCode.objects.create(phone_number=cd['phone'], code=rand_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }
            messages.success(request, 'We sent you a code', 'success')
            return redirect('core:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'core/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == code_instance.code:
                # This method validates the code by datetime to make sure it's not expired
                if code_instance.is_valid():
                    User.objects.create_user(
                        phone_number=user_session['phone_number'],
                        email=user_session['email'],
                        full_name=user_session['full_name'],
                        password=user_session['password']
                    )
                    code_instance.delete()
                    messages.success(request, 'Your information has registered successfully', 'success')
                    return redirect('product:home')
                else:
                    messages.error(request, 'The code has expired. Please try again.', 'danger')
                    return redirect('core:register')
            else:
                messages.error(request, 'This code is WRONG!', 'danger')
                return redirect('core:verify_code')
        return redirect('product:home')
