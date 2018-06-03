'''
Created on 2018. 5. 20.

@author: main
'''
#모델클래스와 관련된 입력양식 클래스를 만드는 파일

#모델클래스와 연관된 입력양식클래스를 만들때 사용
from django.forms.models import ModelForm 
from . import models #. : 현재위치

class QuestionForm(ModelForm):
    class Meta: #어떤 모델클래스를 사용하는지, 어떤속성을 사용하는지
        #model : 내가 연결할 모델 클래스(필수 항목)
        #fields, exclude 중 택 1
        #fields : 모델클래스의 속성중 사용자가 작성해야하는 것을 명시
        #exclude : 모델클래스의 속성중 명시한 속성을 제외한 속성들을 사용자가 작성
        model = models.Question #Question 클래스를 사용하는 것을 명시
        fields = ['question_text' ,'image',] #변수이름과 동일한 문자열 작성
        #exclude=['pub_date','customuser',]
        
class ChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        #fields =['question','choice_text',]
        exclude = ['votes','question', ]
    
    
class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields=['text','image',]
    
    
    
    
    
    
    
    