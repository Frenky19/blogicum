from django.urls import include, path

from . import views


app_name = 'blog'


posts_url = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        '<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path(
        '<int:post_id>/comment/<int:comment_id>/edit_comment/',
        views.edit_comment, name='edit_comment'),
    path(
        '<int:post_id>/comment/<int:comment_id>/delete_comment/',
        views.edit_comment,
        name='delete_comment'
    ),
]

profile_url = [
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile, name='profile'),
]

urlpatterns = [
    path('profile/', include(profile_url)),
    path('posts/', include(posts_url)),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path('', views.index, name='index'),
]
