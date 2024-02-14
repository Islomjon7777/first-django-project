from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreatePostForm, RegisterForm, ProfileForm, CommentForm
from .models import *

# Create your views here.
# HOME VIEW
@login_required(login_url="login/")
def HomeView(request):
    post_yaxshi = PostlarModel.objects.filter(turi="yaxshi")
    post_yaxshi_count = PostlarModel.objects.filter(turi="yaxshi").count()
    post_yomon = PostlarModel.objects.filter(turi="yomon")
    post_yomon_count = PostlarModel.objects.filter(turi="yomon").count()

    ctx = {
        'yaxshi': post_yaxshi,
        'yaxshi_count': post_yaxshi_count,
        'yomon': post_yomon,
        'yomon_count': post_yomon_count,
    }

    return render(request, 'home.html', ctx)




# LOGIN UCHUN VIEW
def LoginView(request):
    if request.POST:
        userName = request.POST['username']
        userPassword = request.POST['password']
        user = authenticate(request, username=userName, password=userPassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Akkaunt muvofaqiyatli kirdingiz.")
            return redirect('/')
        else:
            messages.success(request, "Login yoki parol xato.")
            return redirect('login')
    else:
        return render(request, 'login.html')



# LOGOUT UCHUN VIEW
def LogoutView(request):
    logout(request)
    return render(request, 'home.html')


# REGISTRATSIYA UCHUN VIEW
def RegisterView(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkaunt muvoffaqiyatli ro'yxatdan o'tdi.")
            return redirect('login')
        else:
            messages.error(request, "Hamma joyni to'ldiring.")
            return redirect('register')
        
    else:
        form = RegisterForm()
    
    ctx = {
        "forms": form
    }

    return render(request, 'register.html', ctx)


@login_required(login_url='/login')
def ProfileView(request, pk):
    userEdit = Profile.objects.get(user_id=pk)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=userEdit)
        if form.is_valid():
            form.save()
            messages.success(request, "Account muvoffaqiyatli yangilandi!")
            return redirect('profile', pk=userEdit.user_id)
        else:
            messages.error(request, "Hamma joyni to'ldiring!")
            return redirect('profile', pk=userEdit.user_id)
        
    form = ProfileForm(instance=userEdit)

    ctx = {
        "forms": form
    }

    return render(request, 'profile.html', ctx)



# YANGI POST YARATISH UCHUN VIEW
@login_required(login_url='/login')
def CreatePostView(request, pk):
    post_id = Profile.objects.get(user_id=pk)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            profile_title = form.cleaned_data['title']
            profile_text = form.cleaned_data['text']
            profile_img = form.cleaned_data['post_image']
            profile_turi = form.cleaned_data['turi']
            form_data = PostlarModel(profile=post_id, title = profile_title, text = profile_text, post_image = profile_img, turi = profile_turi)
            form_data.save()
            messages.success(request, "Post muvoffaqiyatli joylandi!")
            return redirect('/')
        else:
            messages.error(request, "Iltimos ,hamma joyni to'ldiring")
            return redirect('create_post')

    form = CreatePostForm()

    ctx = { 
        'forms': form
    }

    return render(request, 'create_post.html', ctx)


# POSTS
def PostsView(request, pk):
    user_posts = PostlarModel.objects.filter(profile_id=pk)
    user_posts_count = PostlarModel.objects.filter(profile_id=pk).count()
    print(user_posts)
    ctx = {
        "userPosts": user_posts,
        "userPostsCount": user_posts_count        
    }
    return render(request, "posts.html", ctx)



# POSTNI EDIT QILISH UCHUN VIEW
def newpostupdateView(request, pk):
    edittovar = PostlarModel.objects.get(id=pk)
    if request.POST:
        form =CreatePostForm(request.POST, request.FILES, instance=edittovar)
        if form.is_valid():
            form.save()
            messages.success(request, "Post muvoffaqiyatli yangilandi!")
            return redirect('posts', request.user.id)
        else:
            messages.error(request, "Hamma joyni to'ldiring")
            return redirect('PostEditForm', pk=edittovar.id)
        
    form =CreatePostForm(instance=edittovar)

    ctx = {
        "form": form,
        "pk": pk
    }
    return render(request, 'edit_post.html', ctx)




# POST DELETE UCHUN VIEW
def newpostdeleteView(request, pk):
    tovar = PostlarModel.objects.get(id=pk)
    tovar.delete()

    return redirect('/')

@login_required(login_url='/login')
def CommentView(request,pk):
    post_s = PostlarModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=True)
            data.post = PostlarModel.objects.get(id=pk)
            data.profile = Profile.objects.get(id=request.user.id)
            data.save()
            return redirect('comment', pk)
        else:
            return redirect('comment', pk)
    
    comment_id = CommentModel.objects.filter(post_id=pk)
    comment_id_count = CommentModel.objects.filter(post_id=pk).count()
    form = CommentForm()
    
    ctx = {
        'form': form,
        'posts': post_s,
        'comment_id': comment_id,
        'comment_count': comment_id_count,
    }

    return render(request,'comment.html',ctx)



@login_required(login_url='/login')
def EditCommentsView(request, pk):
    editcomment = CommentModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST, instance=editcomment)
        if form.is_valid():
            form.save()
            messages.success(request, "comment muvoffaqiyatli yangilandi!")
            return redirect('comment', request.user.id)
        else:
            messages.success(request, "comment muvoffaqiyatli yangilandi!")
            return redirect('EditComments', pk=editcomment.id)
        
    form = CommentForm(instance=editcomment)

    ctx = {
        'forms': form,
        'pk': pk
    }
    return render(request, 'edit_comment.html', ctx)