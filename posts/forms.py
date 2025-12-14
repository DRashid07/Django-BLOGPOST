from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border rounded px-3 py-2',
        'placeholder': 'Adınız'
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full border rounded px-3 py-2',
        'rows': 4,
        'placeholder': 'Şərhinizi yazın...'
    }))
