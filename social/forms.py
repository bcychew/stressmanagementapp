from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs={
            'rows': '4',
            'placeholder': 'Enter your text here'
        })
    )
    #image is optional with required = False
    image = forms.ImageField(required = False,
            widget = forms.ClearableFileInput(attrs={
                'multiple': True
            })
    )
    #class returns just body and image from post model
    class Meta:
        model = Post
        fields = ['body', 'image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Comment here'
            }))

    class Meta:
        model = Comment
        fields = ['comment']

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)
    
    
class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


