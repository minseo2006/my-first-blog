'''
Created on 2018. 6. 3.

@author: User
'''
from django.forms.models import ModelForm
from .models import Post,Image

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('pub_date','author',)
    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)
        #아무것도 선택하지 않을 때의 기본값
        self.fields['type'].empty_label=None
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields=('post','image',)
