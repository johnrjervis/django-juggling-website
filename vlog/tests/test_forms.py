from django.test import TestCase
from vlog.forms import CommentForm, EMPTY_COMMENT_ERROR

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
        form = CommentForm(data = {'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_COMMENT_ERROR])

    def test_validation_of_empty_commenter_name_field(self):
        form = CommentForm(data = {'text': 'Some text', 'author': ''})
        self.assertTrue(form.is_valid())

    def test_form_does_not_have_labels(self):
        form = CommentForm()
        self.assertNotIn('label', form.as_p())

    def test_textarea_does_not_have_cols_or_rows(self):
        form = CommentForm()
        self.assertIn('cols=""', form.as_p())
        self.assertIn('rows=""', form.as_p())

