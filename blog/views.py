from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
import datetime
from django.http import HttpResponseNotFound, Http404
# views handles routes


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<view_type>.html i.e blog/post_list.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        # following either method can be applied:

        user = get_object_or_404(User, username=self.kwargs.get('username'))  # shortcut method to get object and "self.kwargs.get('username')" to get username from url
        print(user.id)  # user is user object
        return Post.objects.filter(author=user).order_by('-date_posted')
        
        # qs = Post.objects.filter(author__username=self.kwargs['username'])
        # if qs:
        #     return qs
        # else:
        #     raise Http404(f"User with username {self.kwargs['username']} does not exists")


class PostDetailView(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'  by default django looks for app_name/(model_name)_detail.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     UpdateView):  # UserPassesTestMixin : user should pass certain test conditions and here only author can edit his post
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  # running form valid method in parent class which runs after setting the author

    def test_func(self):
        post = self.get_object()  # gives the post that we are trying to update
        if self.request.user == post.author:  # whether current user is author of the post
            return True
        return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()  # gives the post that we are trying to update
        if self.request.user == post.author:  # whether curent user is auther of the post
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
