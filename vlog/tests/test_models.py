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
        old_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        future_video = self.post_video(video = 'first', pub_date = future_date)
        old_video = self.post_video(video = 'second', pub_date = old_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

        homepage_video = JugglingVideo.get_homepage_video()

        self.assertEqual(homepage_video, current_video)

    def test_get_homepage_class_method_returns_empty_string_if_no_videos_are_available(self):
        """
        The get_homepage_video JugglingVideo class method should return the empty string if no videos are available
        """
        homepage_video = JugglingVideo.get_homepage_video()

        self.assertEqual(homepage_video, '')

    def test_get_archive_videos_class_method_returns_list_of_videos_published_before_current_video(self):
        """
        The get_archive_videos JugglingVideo class method should return
        a list of all videos that were published before the most recent video
        The list should be in reverse order of publication date (i.e. newest first)
        """
        oldest_date = timezone.now() - timedelta(days = 10)
        old_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        oldest_video = self.post_video(video = 'first', pub_date = oldest_date)
        old_video = self.post_video(video = 'second', pub_date = old_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

        archive_videos = JugglingVideo.get_archive_videos()

        self.assertEqual(archive_videos, [old_video, oldest_video])

    def test_get_archive_class_method_returns_an_empty_list_if_no_videos_are_available(self):
        """
        The get_archive_videos JugglingVideo class method should return an empty list if no videos are available
        """
        archive_videos = JugglingVideo.get_archive_videos()

        self.assertEqual(archive_videos, [])

    def test_get_archive_class_method_returns_an_empty_list_if_only_one_video_is_available(self):
        """
        The get_archive_videos JugglingVideo class method should return an empty list if one video is available
        """
        current_video = self.post_video(pub_date = timezone.now())

        archive_videos = JugglingVideo.get_archive_videos()

        self.assertEqual(archive_videos, [])

    def test_get_archive_videos_class_method_ignores_future_videos(self):
        """
        The behavior of get_archive_videos JugglingVideo class method should
        not be affected by videos with a future publication date
        """
        future_date = timezone.now() + timedelta(days = 5)
        old_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        future_video = self.post_video(video = 'first', pub_date = future_date)
        old_video = self.post_video(video = 'second', pub_date = old_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

        archive_videos = JugglingVideo.get_archive_videos()

        self.assertEqual(archive_videos, [old_video])

class VideoAndCommentModelTest(JugglingVideoSiteTest):
    """
    Tests for the video comments database
    """

    def test_comment_text(self):
        """
        Check that a comment's text is saved correctly 
        """
        comment = VideoComment(text = 'First comment!')

        self.assertEqual(comment.text, 'First comment!')

    def test_comment_is_related_to_video(self):
        """
        A comment should be linked to the video that it is posted for
        """
        juggling_video = self.post_video()
        comment = VideoComment(text = 'First comment!', video = juggling_video)
        comment.save()

        self.assertIn(comment, juggling_video.videocomment_set.all())

    def test_cannot_save_a_blank_comment(self):
        """
        An attempt to save a blank comment should raise an exception
        """
        juggling_video = self.post_video()
        comment = VideoComment(text = '', video = juggling_video)

        with self.assertRaises(ValidationError):
            comment.save()
            comment.full_clean()

    def test_duplicate_comments_are_invalid(self):
        """
        Comments that have the same author, video and text attributes should be invalid
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(video = juggling_video, text = 'Nice!', author = 'Site visitor')

        with self.assertRaises(ValidationError):
            comment = VideoComment(video = juggling_video, text = 'Nice!', author = 'Site visitor')
            comment.full_clean()

    def test_can_save_duplicate_comments_for_different_videos(self):
        """
        It should be possible to save the same comment with the same author for different videos
        """
        first_juggling_video = self.post_video(video = 'first')
        second_juggling_video = self.post_video(video = 'second')
        VideoComment.objects.create(video = first_juggling_video, text = 'Nice!', author = 'Site visitor')

        comment = VideoComment(video = second_juggling_video, text = 'Nice!', author = 'Site visitor')
        comment.full_clean() # Should not raise

    def test_can_save_the_same_comments_for_the_same_video_with_different_authors(self):
        """
        It should be possible to save the same comment with the same author for different videos
        """
        juggling_video = self.post_video(video = 'first')
        VideoComment.objects.create(video = juggling_video, text = 'Nice!', author = 'Site visitor')

        comment = VideoComment(video = juggling_video, text = 'Nice!', author = 'Juggling fan')
        comment.full_clean() # Should not raise

    def test_comment_ordering(self):
        """
        VideoComment.objects should return comments in the order that they were saved
        """
        juggling_video = self.post_video()
        comment1 = VideoComment.objects.create(video = juggling_video, text = '#1')
        comment2 = VideoComment.objects.create(video = juggling_video, text = '#2')
        comment3 = VideoComment.objects.create(video = juggling_video, text = '#3')

        self.assertEqual(list(VideoComment.objects.all()), [comment1, comment2, comment3])

    def test_str_representation_of_comments(self):
        """
        Using str() on a comment object should return it's text attribute
        """
        juggling_video = self.post_video()
        comment = VideoComment.objects.create(video = juggling_video, text = 'comment text')

        self.assertEqual(str(comment), 'comment text')


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


