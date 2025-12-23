from django import forms
from .models import Post14, Profile,ContactMessage,Comment,Report

class PostForm(forms.ModelForm):
    class Meta:
        model = Post14
        fields = ['caption', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'placeholder': 'Explain the problem...',
                'rows': 3
            })
        }