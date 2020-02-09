from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import CreateView, UpdateView
# from django.contrib.auth import authenticate, login
from .models import Profile

# from django.contrib.auth.mixins import LoginRequiredMixin
# from shapeshifter.views import MultiModelFormView
# from shapeshifter.mixins import MultiSuccessMessageMixin


class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        form.save()
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # raw_password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=raw_password)
        messages.success(self.request, f' Your Account has been created! you are now able to log in ')
        return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        print(f"POST DATA ={request.POST}")
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f' Your Account has been UPDATED!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

#
# class ProfileUpdateView(MultiModelFormView, MultiSuccessMessageMixin, LoginRequiredMixin):
#     template_name = 'users/profile.html'
#     queryset = Profile.objects.all()
#     form_classes = (UserUpdateForm, ProfileUpdateForm)
#     success_message = 'Your profile has been updated'
#
#     def get_instances(self):
#         profile_instance = Profile.objects.filter(
#             user=self.request.user,
#         ).first(),
#         instances = {
#             'userform': self.request.user,
#             'profileform': profile_instance
#         }
#
#         return instances

    # def get_object(self, queryset=None):
    #     return self.request.user.profile
    #
    # def form_valid(self, form):
    #     # print(form.cleaned_data)
    #     form.save()
    #     return super().form_valid(form)
