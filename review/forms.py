from django import forms
from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80,
                'rows': 10,
                'placeholder':'Description'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Titre'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control'})
        }

class SubscriptionForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            # 'class': 'form-control',
            'placeholder':'Nom d\'utilisateur'})
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('headline', 'rating', 'body')
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'form-control',
                'placeholder':'Titre'}),
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Titre'}),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80,
                'rows': 10,
                'placeholder':'Description'})
        }
