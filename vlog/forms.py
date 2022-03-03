from django import forms
from django.core.exceptions import ValidationError
from vlog.models import VideoComment


EMPTY_COMMENT_ERROR = 'You cannot submit an empty comment.'
DUPLICATE_COMMENT_ERROR = 'That comment has already been posted!'


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

    def __init__(self, for_video, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.video = for_video

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_COMMENT_ERROR]}
            self._update_errors(e)

    def clean_author(self):
        data = self.cleaned_data['author'] if self.cleaned_data['author'] else 'anonymous'
        return data

    class Meta:
        model = VideoComment
        fields = ('author', 'text',)

