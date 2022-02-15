from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from .base import JugglingVideoSiteTest


class VideoModelTest(JugglingVideoSiteTest):
    """
    Tests for the juggling video database
    """

    def test_saving_and_retrieving_videos(self):
        """
        The attributes of a video object should match those that it was saved with 
        """
        first_video = self.post_video(pub_date = timezone.now())

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
        self.assertEqual(first_video.title, first_saved_video.title)
        self.assertEqual(first_video.pub_date, first_saved_video.pub_date)
        self.assertEqual(first_video.author_comment, first_saved_video.author_comment)

    def test_static_filename_attribute_provides_correct_path_to_video_file(self):
        """
        The (non DB) static file attribute of a video object should point to the correct file location
        """
        first_video = self.post_video()

        first_saved_video = JugglingVideo.objects.first()

        self.assertEqual(first_saved_video.get_static_filename(), f'vlog/videos/{first_video.filename}')

    def test_get_approved_comments_method_only_returns_approved_comments(self):
        """
        A video object's self.get_approved_comments() should filter out comments that are not approved
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', video = juggling_video)
        VideoComment.objects.create(text = 'Inappropriate comment!', video = juggling_video, is_approved = False)
        VideoComment.objects.create(text = 'Nice!', video = juggling_video)

        self.assertEqual(len(juggling_video.get_approved_comments()), 2)
        for comment in juggling_video.get_approved_comments():
            self.assertTrue(comment.is_approved)

    def test_get_absolute_url(self):
        """
        Tests the absolute URL retrieval for the JugglingVideo model
        """
        juggling_video = self.post_video()

        self.assertEqual(juggling_video.get_absolute_url(), reverse('vlog:detail', args = [juggling_video.id]))

    def test_get_homepage_class_method_returns_most_recently_published_current_video(self):
        """
        The get_homepage_video JugglingVideo class method should return the correct video for the homepage
        """
        future_date = timezone.now() + timedelta(days = 5)
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        future_video = self.post_video(video = 'first', pub_date = future_date)
        older_video = self.post_video(video = 'second', pub_date = older_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

        homepage_video = JugglingVideo.get_homepage_video()

        self.assertEqual(homepage_video, current_video)

    def test_get_homepage_class_method_returns_empty_string_if_no_videos_are_available(self):
        """
        The get_homepage_video JugglingVideo class method should return the empty string if no videos are available
        """
        homepage_video = JugglingVideo.get_homepage_video()

        self.assertEqual(homepage_video, '')


class VideoAndCommentModelTest(JugglingVideoSiteTest):
    """
    Tests for the video comments database
    """

    def test_saving_and_retrieving_comments(self):
        """
        The attributes of a comment object should match those that it was saved with 
        """
        juggling_video = self.post_video()
        first_comment = VideoComment()
        first_comment.text = 'First comment!'
        first_comment.video = juggling_video
        comment_date = timezone.now()
        first_comment.date = comment_date
        first_comment.save()
        second_comment = VideoComment()
        second_comment.text = 'Nice video!'
        second_comment.author = 'Site visitor'
        second_comment.video = juggling_video
        second_comment.is_approved = False
        second_comment.save()

        saved_comments = VideoComment.objects.all()
        first_saved_comment = saved_comments[0]
        second_saved_comment = saved_comments[1]

        self.assertEqual(saved_comments.count(), 2)
        self.assertEqual(first_saved_comment.text, 'First comment!')
        self.assertEqual(first_saved_comment.author, 'anonymous')
        self.assertEqual(first_saved_comment.video, juggling_video)
        self.assertEqual(first_saved_comment.date, comment_date)
        self.assertEqual(first_saved_comment.is_approved, True)
        self.assertEqual(second_saved_comment.text, 'Nice video!')
        self.assertEqual(second_saved_comment.author, 'Site visitor')
        self.assertEqual(second_saved_comment.video, juggling_video)
        self.assertEqual(second_saved_comment.is_approved, False)

    def test_cannot_save_a_blank_comment(self):
        """
        Tests that an attempt to save a blank comment raises an exception
        """
        juggling_video = self.post_video()
        comment = VideoComment(video = juggling_video, text = '')

        with self.assertRaises(ValidationError):
            comment.save()
            comment.full_clean()


class AcknowledgementsModelTest(TestCase):
    """
    Tests for the acknowledgements database
    """

    def test_saving_and_retrieving_acknowledgements(self):
        """
        The attributes of an acknowledgement object should match those that it was saved with 
        """
        first_acknowledgement = Acknowledgement.objects.create(name ='Django', link ='https://www.djangoproject.com/', description = 'This site was built using the Django framework.')
        second_acknowledgement = Acknowledgement.objects.create(name ='The Mozilla Development Network (MDN)', link = 'https://developer.mozilla.org/en-US/', description = 'MDN provide courses covering various web development topics, including HTML, CSS & JavaScript.')

        saved_acknowledgements = Acknowledgement.objects.all()
        first_saved_acknowledgement = saved_acknowledgements[0]
        second_saved_acknowledgement = saved_acknowledgements[1]

        self.assertEqual(saved_acknowledgements.count(), 2)
        self.assertEqual(first_saved_acknowledgement.name, 'Django')
        self.assertEqual(first_saved_acknowledgement.link, 'https://www.djangoproject.com/')
        self.assertEqual(first_saved_acknowledgement.description, 'This site was built using the Django framework.')
        self.assertEqual(second_saved_acknowledgement.name, 'The Mozilla Development Network (MDN)')
        self.assertEqual(second_saved_acknowledgement.link, 'https://developer.mozilla.org/en-US/')
        self.assertEqual(second_saved_acknowledgement.description, 'MDN provide courses covering various web development topics, including HTML, CSS & JavaScript.')


