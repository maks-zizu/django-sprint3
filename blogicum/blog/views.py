from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


POSTS_COUNT_ON_INDEX = 5


def index(request):
    post_list = (
        Post.objects.select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        .order_by('-pub_date')[:POSTS_COUNT_ON_INDEX]
    )
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ),
        pk=id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    post_list = (
        category.posts
        .select_related('author', 'location', 'category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )
        .order_by('-pub_date')
    )
    return render(
        request, 'blog/category.html',
        {'category': category, 'post_list': post_list}
    )
