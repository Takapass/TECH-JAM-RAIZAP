from django import forms
from .models import Idea
from django.contrib.auth.models import User


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'idea-textarea',
                'placeholder': '今の健康アイデアを投稿',
            }),
        }

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }