from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag, Like
from .forms import BlogForm
from django.urls import reverse


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user
    return render(request,'home.html',{'page_obj':page_obj, 'user' : user})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    tags = blog.tag.all()
    likes = Like.objects.filter(blog=blog)
    print(likes)

    return render(request,'detail.html',{'blog':blog , 'comments':comments, 'tags' : tags, 'likes': likes})

def new(request):
    tags = Tag.objects.all()
    return render(request,'new.html', { 'tags' : tags })

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user
    new_blog.save()

    tags = request.POST.getlist('tags')

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)

    return redirect('detail', new_blog.id)
    # return render(request, 'detail.html', {'blog':new_blog})

# def create(request):
#     form = BlogForm(request.POST)
#
#     if form.is_valid():
#         new_blog = form.save(commit=False)
#         new_blog.save()
#         return redirect('detail', new_blog.id)
#
#     return render(request, 'new.html')

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id) # print() 해보기

    #내가 쓴글이 아니라면 edit x
    if request.user != edit_blog.author:
        return redirect('home')
    
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

# def update(request, blog_id):
#     old_blog = get_object_or_404(Blog, pk=blog_id)
#     form = BlogForm(request.POST, instance=old_blog)

    # 클라이언트가 유효한 값을 입력한 경우
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)

    return render(request, 'new.html', {'old_blog':old_blog})


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')


#댓글 달기
def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user

    comment.save()

    return redirect('detail', blog_id)

def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', { 'blog' : blog })

def like(request, blog_id):

    # 로그인하지 않은 유저
    if request.user.is_anonymous:
        return redirect("login")
    
    # 로그인한 유저인데, 해당 유저가 해당 글에 좋아요를 눌렀었다면
    myLike = Like.objects.filter(user=request.user, blog_id=blog_id)
    if myLike:
        myLike.delete()
        return redirect("detail", blog_id)
    
    # 로그인한 유저인데, 해당 유저가 해당 글에 좋아요를 누른 적이 없다면
    like = Like()
    like.blog = get_object_or_404(Blog, pk=blog_id)
    like.user = request.user
    like.save()
    return redirect('detail', blog_id)

    