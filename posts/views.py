from django.shortcuts import render, redirect
from django.db.models import Q 
from .models import Category, Post, Author
from .forms import CommentForm

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    from .models import Comment, PostLike, Favourite
    post = Post.objects.get(slug = slug)
    
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    latest = Post.objects.order_by('-timestamp')[:3]
    total_likes = post.likes.count()
    user_has_liked = False
    user_has_favourited = False
    if request.user.is_authenticated:
        user_has_liked = PostLike.objects.filter(post=post, user=request.user).exists()
        user_has_favourited = Favourite.objects.filter(post=post, user=request.user).exists()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            
            Comment.objects.create(
                post=post,
                name=form.cleaned_data['name'],
                body=form.cleaned_data['body'],
                user=request.user if request.user.is_authenticated else None
            )
            return redirect('post', slug=slug)
    else:
        form = CommentForm()  
    
    context = {
        'post': post,
        'latest': latest,
        'form' : form,
        'comments': post.comments.all(),
        'total_likes':total_likes,
        'user_has_liked':user_has_liked,
        'user_has_favourited': user_has_favourited,
    }
    return render(request, 'post.html', context)

def about(request):
    from .models import About
    about_content = About.objects.first()
    context = {
        'about': about_content
    }
    return render(request, 'about_page.html', context)

def search(request):
    from .models import Comment, Tag
    query = request.GET.get('q')
    
    if query:
        # Post axtarışı: title, overview, content, author username
        queryset = Post.objects.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query) |
            Q(author__user__username__icontains=query)
        ).distinct()
        
        # Comment-lərdə axtarış - post-ları tap
        comment_posts = Post.objects.filter(
            Q(comments__name__icontains=query) |
            Q(comments__body__icontains=query)
        ).distinct()
        
        # Tag-lərdə axtarış - post-ları tap
        tag_posts = Post.objects.filter(
            tags__name__icontains=query
        ).distinct()
        
        # Hamısını birləşdir (union)
        queryset = (queryset | comment_posts | tag_posts).distinct()
    else:
        queryset = Post.objects.none()
    
    context = {
        'object_list': queryset,
        'query': query,
        'result_count': queryset.count()
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)


def like_post(request, slug):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    from .models import PostLike
    post = Post.objects.get(slug=slug)
    
    like = PostLike.objects.filter(post=post, user=request.user).first()
    
    if like:
        like.delete()
    else:
        PostLike.objects.create(post=post, user=request.user)
    
    return redirect('post', slug=slug)




def favourite_post(request, slug):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    from .models import Favourite
    post = Post.objects.get(slug=slug)
    
    favourite = Favourite.objects.filter(post=post, user=request.user).first()
    
    if favourite:
        favourite.delete()
    else:
        Favourite.objects.create(post=post, user=request.user)
    
    return redirect('post', slug=slug)



def my_favourites(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    from .models import Favourite
    favourites = Favourite.objects.filter(user=request.user).select_related('post')
    
    context = {
        'favourites': favourites,
    }
    return render(request, 'favourites.html', context)


def tags_list(request):
    from .models import Tag
    tags = Tag.objects.all().order_by('name')
    
    context = {
        'tags': tags,
    }
    return render(request, 'tags_list.html', context)


def posts_by_tag(request, tag_id):
    from .models import Tag
    tag = Tag.objects.get(id=tag_id)
    posts = Post.objects.filter(tags=tag).order_by('-timestamp')
    
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'posts_by_tag.html', context)