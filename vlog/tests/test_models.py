from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from datetime import timedelta


class VideoModelTest(TestCase):
    """
    Tests for the juggling video database
    """

    def test_saving_and_retrieving_videos(self):
        """
        The attributes of a video object should match those that it was saved with 
        """
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle', pub_date = timezone.now(), author_comment = 'This video was recorded in hotel quarantine')

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
        self.assertEqual(first_video.title, first_saved_video.title)
        self.assertEqual(first_video.pub_date, first_saved_video.pub_date)
        self.assertEqual(first_video.author_comment, first_saved_video.author_comment)

class VideoAndCommentModelTest(TestCase):
    """
    Tests for the video comments database
    """

    def test_saving_and_retrieving_comments(self):
        """
        The attributes of a comment object should match those that it was saved with 
        """
        juggling_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle')
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
        juggling_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle')
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


