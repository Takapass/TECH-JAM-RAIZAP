from django import forms
from .models import Idea

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