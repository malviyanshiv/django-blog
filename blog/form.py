from django import forms
from blog.models import Comment, Subscribe

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SubscribForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ('name', 'email')