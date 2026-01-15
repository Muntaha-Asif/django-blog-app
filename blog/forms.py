from django import forms
from .models import Comment, Profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'comment-textarea'
            })
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'website', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
        }