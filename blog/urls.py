from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, \
    BlogDeleteView, Toggle_Activity_Blog, BlogDraftListView


app_name = 'blog'


urlpatterns = [
    path('', BlogListView.as_view(), name='blogs'),
    path('drafts', cache_page(60)(BlogDraftListView.as_view()), name='blog_drafts'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/toggle/<slug:slug>/', Toggle_Activity_Blog.as_view(), name='toggle_activity_blog'),

]
