from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import render


class NewsList(ListView):
    model = Post
    ordering = '-add_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-add_date'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exeption = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin,LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


@login_required
def subscribe(request, pk1, pk2):
    post = Post.objects.get(id=pk1)
    user = request.user
    category = Category.objects.get(id=pk2)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей в категории'
    return render(request, 'subscribe.html', {'post': post, 'category': category, 'message': message})


@login_required
def unsubscribe(request, pk1, pk2):
    post = Post.objects.get(id=pk1)
    user = request.user
    category = Category.objects.get(id=pk2)
    category.subscribers.remove(user)
    message = 'Вы успешно отписались от рассылки новостей в категории'
    return render(request, 'unsubscribe.html', {'post': post, 'category': category, 'message': message})
