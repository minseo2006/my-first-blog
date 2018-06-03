from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from polls.models import Question, Choice
from django.http import HttpResponseRedirect #특정 주소로 이동
from django.urls import reverse #별칭을 통해 url주소 획득
from datetime import datetime #시간에 관련된 파이썬 내장 함수
from customuser.models import CustomUser
#from . import forms
#from .forms import *
from polls.forms import ChoiceForm,QuestionForm, CommentForm
#HttpResponseRedirect(reverse('polls:detail',args=(question_id.id, ) ) )
# Create your views here.

def index(request):
    data = Question.objects.all()
    return render(request, 'polls/index.html', {'data':data})
    # return HttpResponse('응답 완료')

def detail(request, question_id):
    if request.method == "GET":
        question_data = get_object_or_404(Question,pk=question_id)
        #댓글 폼 생성
        form = CommentForm()
        #question_data = Question.objects.get(id=question_id)
        # choice_data = Choice.objects.filter(question=question_id)
        context = {
            'form' : form,
            'question_data':question_data,
            # 'choice_data':choice_data
        }
        return render(request, 'polls/detail.html', context)
        # return HttpResponse('question_id : {}'.format(question_id))
    elif request.method == "POST":
        form = CommentForm( request.POST, request.FILES )
        if form.is_valid():
            #Question 객체 찾기
            question = get_object_or_404(Question,pk=question_id)
            #CustomUser 객체 찾기
            customuser = get_object_or_404(CustomUser,pk=request.session['username'])
            obj = form.save(commit=False)
            obj.question = question
            obj.customuser = customuser
            obj.save()
            return HttpResponseRedirect( reverse('polls:detail', args=(question_id, ) )  )
        
        
        
from django.db.models import F #race condition 방지

def vote(request, question_id):
    #if request.method=="GET": GET방식으로 요청했을 때만 처리
    if request.method =="POST": #request.method : 클라이언트가 어떤방식으로 뷰를 요청했는지 확인
        data = Choice.objects.get(id__exact=request.POST.get('vote'), question=question_id)
        data.votes = F('votes') + 1
        data.save()
         
        return HttpResponseRedirect( reverse('polls:results',args=(question_id, )  )  )
    else:
        return HttpResponseRedirect( reverse('polls:detail', args=(question_id,) ) )
    #return redirect('/polls/{}/results/'.format(question_id))

def results(request, question_id):
    data = Question.objects.get(id=question_id)
    context = {
        'data':data
    }
    return render(request, 'polls/results.html', context)
    # return HttpResponse('question_id : {}'.format(question_id))


def registerQ(request):
    #로그인 여부를 체크하는 코드
    if 'loginstate' in request.session:
        if request.method =="GET": #해당 뷰를 GET 방식으로 요청시(페이지 접근)
            #QuestionForm 객체를 생성 - HTML에서 form 태그 컨텐츠안에 넣으면 됨
            obj = QuestionForm() 
            return render(request,'polls/registerQ.html', {'form' : obj } )
        else: #해당 뷰를 POST방식으로 요청시
            #request.POST.get("") form내에 있는 특정 변수값을 가져올때
            #request.POST form내에 있는 모든 값을 사용
            #POST방식으로 온 데이터를 QuestionForm에 삽입
            obj = QuestionForm(request.POST,request.FILES)
            #obj.is_valid() : 사용자가 <form>에 있는 양식을 잘 작성했는지 확인(True,False)
            if obj.is_valid():#값이 유효한가?
                #obj.save() : QuestionForm을 Question 객체로 변환 후,데이터베이스에 저장
                #obj.save(commit = False) : QuestionForm을 Question객체로 변환
                user = get_object_or_404(CustomUser, pk = request.session['username'])     
                
                question = obj.save(commit=False)
                question.pub_date = datetime.now()
                question.customuser = user #CustomUser 객체를 매칭
                question.save() #데이터베이스에 반영
                return HttpResponseRedirect(reverse('polls:index') )
            else: #값이 유효하지 않을때 처리
                return render(request,'polls/registerQ.html', 
                              {'form' : obj, 'error_message' : "비정상적인 값입니다."} )
    else:#세션에 loginstate값이 없는 경우(비로그인 상태) 
        return render(request,'polls/error.html',
                      {'error':'로그인 후 접근할 수 있는 페이지입니다.'})
def registerC(request,question_id):
    
    if 'username' not in request.session:
        return render(request,'polls/error.html',
                      {'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    question = get_object_or_404(Question, pk=question_id)    
    if question.customuser.id == request.session['username']:
        if request.method =="GET": #해당 뷰를 GET 방식으로 요청시(페이지 접근)
            #QuestionForm 객체를 생성 - HTML에서 form 태그 컨텐츠안에 넣으면 됨
            #get_object_or_404(모델클래스명, pk=id값을 가진 변수)
            #from django.shortcuts import get_object_or_404
            #입력한 모델클래스에서 객체를 찾아서 없는경우 404Error 띄워줌
            
            obj = ChoiceForm() 
            return render(request,'polls/registerC.html', 
                          {'form' : obj , 'question' : question} )
        else: #해당 뷰를 POST방식으로 요청시
            #request.POST.get("") form내에 있는 특정 변수값을 가져올때
            #request.POST form내에 있는 모든 값을 사용
            #POST방식으로 온 데이터를 QuestionForm에 삽입
            obj = ChoiceForm(request.POST)
            #obj.is_valid() : 사용자가 <form>에 있는 양식을 잘 작성했는지 확인(True,False)
            if obj.is_valid():#값이 유효한가?
                #obj.save() : QuestionForm을 Question 객체로 변환 후,데이터베이스에 저장
                #obj.save(commit = False) : QuestionForm을 Question객체로 변환
                choice = obj.save(commit=False)
                choice.question = question #question객체를 넘겨줘야함
                choice.save()
                return HttpResponseRedirect(reverse('polls:detail', args=(question_id,) ) )
            else: #값이 유효하지 않을때 처리
                return render(request,'polls/registerC.html', 
                              {'form' : obj, 'error_message' : "비정상적인 값입니다."} )
    else:#현재 글과 로그인된 유저의 이름이 다름
        return render(request,'polls/error.html',
                      {'error':'본인이 작성한 글이 아닙니다'})

def deleteQ(request, question_id):
    #비로그인일 때 제어
    if 'username' not in request.session:
        return render(request,'polls/error.html',
                      {'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    #글쓴이와 다른 사람이 로그인 했을 때 제어
    obj = get_object_or_404(Question,pk=question_id)
    if obj.customuser.id == request.session['username']:
        obj.delete() #객체를 데이터베이스에서 삭제
        return HttpResponseRedirect( reverse('polls:index') )
    else:
        return render(request,'polls/error.html',
                      {'error':'본인이 작성한 글만 삭제할 수 있습니다.'})
def deleteC(request, choice_id):
    #비로그인일 때 제어
    if 'username' not in request.session:
        return render(request,'polls/error.html',
                      {'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    #글쓴이와 다른 사람이 로그인 했을 때 제어    
    obj = get_object_or_404(Choice,pk=choice_id)
    if obj.question.customuser.id == request.session['username']:
    #obj : choice객체 #obj.question : choice 객체와 연결된 question 객체
    #obj.question.id : choice 객체와 연결된 question 객체의 id값
        question_id = obj.question.id
        obj.delete()
        return HttpResponseRedirect( reverse('polls:detail', args=(question_id,) ) )
    else:
        return render(request,'polls/error.html',
                      {'error':'본인이 등록한 글만 삭제할 수 있습니다.'})


def search(request):
    #GET방식으로 들어온 데이터를 읽을때 사용
    type = request.GET.get('type','0')
    content = request.GET.get('content', '' )
    #질문의 제목으로 검색
    if type == '0':
        #쿼리셋 생성
        q = Question.objects.filter(question_text__contains = content)
        return render(request, 'polls/search.html', 
                      {'resultlist' : q, 'content' : content} )
    #글쓴이로 검색
    elif type == '1':
        #CustomUser의 id값이 content와 동일한 객체를 추출
        user = CustomUser.objects.filter(id=content)
        #customuser변수의 값이 user객체와 동일한 Question객체를 추출
        q = Question.objects.filter(customuser__in=user)
        return render(request,'polls/search.html',
                      {'resultlist':q,'content':content})
    #투표수로 검색
    #Choice에 관한 검색결과이므로 새로운 html파일을 생성해야함
    elif type =='2':
        content = int(content)
        q = Choice.objects.filter(votes__gt=content)
        return render(request,'polls/searchC.html',
                      {'resultlist':q,'content':content})
    else:#개발자가 설정한 type 외에 값이 들어온 경우
        return render(request, 'polls/error.html',
                      { 'error' : "검색타입이 정상적이지 않습니다"} )












