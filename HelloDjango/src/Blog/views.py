from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.forms.forms import Form
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from email.mime import image
# Create your views here.
#자유게시판 메인페이지
#Post객체를 10개씩 보여줌
#다음페이지 : 다음 객체 10개를 보여줌
#이전페이지 : 이전 객체 10개를 보여줌
def index(request):
    if request.method=="GET":
        index = int(request.GET.get('index',0))
        
        #Post 객체 가져오기
        objs = Post.objects.all()
        max = len(objs) #전체 객체 개수
        print(index,max)
        #현재 요청한 페이지의 첫번째 객체의 순서가 Post 객체 개수보다 작은가?
        data = None
        if index*10 < max: 
            if index*10 + 9 < max:
                data = objs[index*10 : index*10+10]
                nextPage = index + 1
            else:
                data = objs[index*10 : ]
                nextPage = -1 
        else:
            return render(request,'polls/error.html',
                          {"error":"요청한 페이지가 없습니다."})
        previousPage = index - 1
        return render(request,"blog/index.html",
                      {'data':data, 'nextPage' : nextPage,
                        'previousPage': previousPage})
    else:
        return render(request,"polls/error.html", 
                      {'error' : "잘못된 접근입니다."})
        
def detail(request, post_id):
    obj = get_object_or_404(Post, pk = post_id)
    return render(request,'blog/detail.html',
                  {'obj':obj})
@login_required
def posting(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            for f in request.FILES.getlist('images'):
                file = Image(post=obj, image = f)
                file.save()
            for f in request.FILES.getlist('files'):
                file = File(post=obj, file = f)
                file.save()
            return HttpResponseRedirect( reverse('blog:detail',args=(obj.id,) ) )
        else:
            return render(request,"blog:posting.html")
            
    elif request.method =="GET":
        form = PostForm()
        return render(request,'blog/posting.html',{'form':form})







@login_required
def post_delete(request,post_id):
    obj = get_object_or_404(Post,pk=post_id)
    if request.user == obj.author:
        obj.delete()
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return render (request, 'polls:error.html', {'error':'본인이 작성한 글만 삭제할 수 있습니다.',"mainurl": reverse('blog:index')})
    
@login_required
def post_update(request,post_id):
    obj = get_object_or_404(Post,pk=post_id)
    if obj.author != request.user:
        return render(request, "polls/error.html", {'error':"자신이 작성한 글만 수정할 수 있습니다.", 'mainurl':reverse('blog/index')})
    if request.method=="POST":
        form = PostForm(request.POST, instance = obj)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog:detail',args=(post.id, )))
        
        else:
            return render(request,"blog/update.html",{'form':form,'error':"유효하지 않음."})
        
    elif request.method=="GET":
        form = PostForm(instance = obj)
        return render(request,"blog/update.html",{'form':form})








