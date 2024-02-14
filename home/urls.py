from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView, name='register'),
    path('profile/<int:pk>/', ProfileView, name='profile'),
    path('create-post/<int:pk>/', CreatePostView, name='create_post'),
    path('posts/<int:pk>/', PostsView, name='posts'),
    path('comment/<int:pk>', CommentView, name='comment'),
    path('edit-comments/<int:pk>/', EditCommentsView, name='edit_comments'),
    path('postDelete/<int:pk>/', newpostdeleteView, name='PostDeleteForm'),
    path('postUpdate/<int:pk>/', newpostupdateView, name='PostEditForm'),
]