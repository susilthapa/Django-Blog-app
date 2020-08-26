from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
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
from django.http import HttpResponseNotFound, Http404, HttpResponseForbidden, JsonResponse, HttpResponse
import json
from django.core import serializers

from .forms import CommentCreationForm

from django.contrib.auth.decorators import login_required

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
    # form_class = CommentCreationForm

    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        id = data['id']
        post = get_object_or_404(Post, id=id)
        text = data['comment']
        print(f'POST ID= {id}')
        comment = Comment()
        comment.author = self.request.user            
        comment.post = post
        comment.text = text
        comment.save()

        new_comment = post.comments.first()
        author = new_comment.author.username
        image = new_comment.author.profile.image.url
        new_text = new_comment.text
        date = new_comment.created_date.strftime("%b %d, %Y")
        print(date)

        data = {
            'count': post.comments.count(),
            'author': author,
            'image': image,
            'text': text,
            'date': date
        }
        # data = serializers.serialize('json', data)
        # return HttpResponse(data, content_type="application/json")
        return JsonResponse(data, safe=False)

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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form, id):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=id)
        return super().form_valid(form)

# class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
#     model = Comment

#     id = 0
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


#     def post(self, request, *args, **kwargs):
#         data = json.loads(self.request.body)
#         id = (data['id'])
#         print(f'DELETE {data}')
#         return id

#     def test_func(self):
#         commant = self.get_object(id)
#         if self.request.user == commant.author:
#             return True
#         return False

#     def get_object(self, id):
#         print(f'DELETE {id}')
#         return self.get_queryset().filter(id=id).get()

#     def get_success_url(self):
#         return self.request.path


@login_required
def delete_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        print(f'DELETE ID = {id}')
        comment = Comment.objects.get(id=id)
        post_id = comment.post.id
        print(f'REQ USER {request.user}')
        print(f'CMT AUTHOR {comment.author}')
        if request.user == comment.author:
            comment.delete()
            data = {
                'count': Comment.objects.filter(post__id = post_id).count()
            }
            return  JsonResponse(data, safe=False)
        else:

            return  HttpResponseForbidden()


@login_required
def like_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        post = get_object_or_404(Post, id=id)
        liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            liked=True
        data = {
            'total_likes': post.total_likes,
            'liked': liked
        }

        return JsonResponse(data, safe=False)



