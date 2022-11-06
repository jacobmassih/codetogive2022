from django.forms import ModelForm
from .models import Topic
from django import forms


class UploadForm(ModelForm):
    author = forms.TextInput()
    title = forms.TextInput()
    description = forms.Textarea()
    city = forms.TextInput()
    label = forms.TextInput()

    class Meta:
        model = Topic
        fields = ['author', 'title', 'description', 'city', 'label']


class CommentForm(ModelForm):
    author = forms.TextInput()
    comment = forms.TextInput()
