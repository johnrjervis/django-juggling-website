from django.test import TestCase
from vlog.forms import CommentForm, EMPTY_COMMENT_ERROR
from vlog.models import JugglingVideo, VideoComment


class ItemFormTest(TestCase):

    def test_form_comment_comment_box_textarea_has_correct_attributes(self):
        form = CommentForm()
        self.assertIn('name="text"', form.as_p())
        self.assertIn('placeholder="Enter your comment"', form.as_p())
        self.assertIn('class="comments_box green_border"', form.as_p())

    def test_form_comment_commenter_name_input_has_correct_attributes(self):
        form = CommentForm()
        self.assertIn('name="author"', form.as_p())
        self.assertIn('placeholder="Enter your name (optional)"', form.as_p())
        self.assertIn('class="commenter_name green_border"', form.as_p())

    def test_validation_of_empty_comment(self):
        """
        The form should be invalid if the comment text field is empty
        """
        form = CommentForm(data = {'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_COMMENT_ERROR])

    def test_validation_of_empty_commenter_name_field(self):
        """
        The form should be valid even if the comment author field is empty
        """
        form = CommentForm(data = {'text': 'Some text', 'author': ''})
        self.assertTrue(form.is_valid())

    def test_form_does_not_have_labels(self):
        form = CommentForm()
        self.assertNotIn('label', form.as_p())

    def test_textarea_does_not_have_cols_or_rows(self):
        form = CommentForm()
        self.assertIn('cols=""', form.as_p())
        self.assertIn('rows=""', form.as_p())

    def test_form_can_save_a_comment(self):
        """
        The form should be able to save a comment object to the database
        """
        juggling_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')
        form = CommentForm(data = {'text': 'Some text', 'author': 'Someone'})
        new_comment = form.save(for_video = juggling_video)
        self.assertEqual(new_comment, VideoComment.objects.first())
        self.assertEqual(new_comment.text, 'Some text')
        self.assertEqual(new_comment.author, 'Someone')
        self.assertEqual(new_comment.video, juggling_video)

    def test_comment_author_is_anonymous_if_no_author_is_supplied(self):
        """
        When a form is saved with an empty author field, the comment's author attribute should be 'anonymous'
        """
        juggling_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')
        form = CommentForm(data = {'text': 'Some text', 'author': ''})
        new_comment = form.save(for_video = juggling_video)
        self.assertEqual(new_comment.author, 'anonymous')

