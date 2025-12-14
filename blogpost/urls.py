from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts.views import homepage, post, about, search, postlist, allposts, like_post, favourite_post, my_favourites

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('post/<slug>/', post, name='post'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('postlist/<slug>/', postlist, name='postlist'), 
    path('posts/', allposts, name='allposts'),
    path('like/<slug>/', like_post, name='like_post'),
    path('favourite/<slug>/', favourite_post, name='favourite_post'),
    path('my-favourites/', my_favourites, name='my_favourites'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
