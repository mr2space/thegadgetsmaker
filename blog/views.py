from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import BlogForm
from home.templatetags import url
from .models import Blog

def index(request):
    param = url.setPara(request,page_name="Blog")
    blogs = Blog.objects.all()
    param["blogs"] = blogs
    return render(request,"blog/blogs.html",param)

@login_required(login_url="/auth/")
def addArtical(request):
    param = url.setPara(request, "")
    # TODO:URL ACTIVE
    if request.method != 'POST':
        param['form'] = BlogForm()
        return render(request, "blog/new_blog.html", param)
    form = BlogForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return redirect(f"/blog/{form.auto_id}")
    return HttpResponse("form not valid")


def showBlog(request,id):
    param=url.setPara(request,"")
    blog = Blog.objects.filter(id=id)
    param['blog'] = blog
    param['blog'] = param['blog'][0]

    return render(request, "blog/blog.html",param)