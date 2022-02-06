from django import forms
from vlog.models import VideoComment

EMPTY_COMMENT_ERROR = 'You cannot submit an empty comment.'

class CommentForm(forms.models.ModelForm):
    author = forms.CharField(
        widget = forms.fields.TextInput(
            attrs = {
                'placeholder': 'Enter your name (optional)',
                'class': 'commenter_name green_border',
            }
        ),
        required = False, 
        label = '',
    )

    text = forms.CharField(
        widget = forms.fields.Textarea(
            attrs = {
                'placeholder': 'Enter your comment',
                'class': 'comments_box green_border',
                'cols': '',
                'rows': '',
            },
        ),
        label = '',
        error_messages = {
            'required': EMPTY_COMMENT_ERROR,
        },
    )

    class Meta:
        model = VideoComment
        fields = ('author', 'text',)

