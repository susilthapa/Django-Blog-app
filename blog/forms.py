from blog.models import Comment

from django import forms


class CommentCreationForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']