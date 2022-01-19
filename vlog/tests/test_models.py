from django.test import TestCase
from django.utils import timezone
from vlog.models import JugglingVideo, VideoComment


class VideoModelTest(TestCase):
    """
    Tests for the juggling video database
    """

    def test_saving_and_retrieving_videos(self):
        """
        The attributes of a video object should match those that it was saved with 
        """
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle', pub_date = timezone.now())

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
        self.assertEqual(first_video.title, first_saved_video.title)
        self.assertEqual(first_video.pub_date, first_saved_video.pub_date)


class VideoAndCommentModelTest(TestCase):
    """
    Tests for the video comments database
    """

    def test_saving_and_retrieving_comments(self):
        juggling_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle', pub_date = timezone.now())
        first_comment = VideoComment()
        first_comment.text = 'First comment!'
        first_comment.video = juggling_video
        first_comment.save()
        second_comment = VideoComment()
        second_comment.text = 'Nice video!'
        second_comment.author = 'Site visitor'
        second_comment.video = juggling_video
        second_comment.save()

        saved_comments = VideoComment.objects.all()
        first_saved_comment = saved_comments[0]
        second_saved_comment = saved_comments[1]

        self.assertEqual(saved_comments.count(), 2)
        self.assertEqual(first_saved_comment.text, 'First comment!')
        self.assertEqual(first_saved_comment.author, 'anonymous')
        self.assertEqual(first_saved_comment.video, juggling_video)
        self.assertEqual(second_saved_comment.text, 'Nice video!')
        self.assertEqual(second_saved_comment.author, 'Site visitor')
        self.assertEqual(second_saved_comment.video, juggling_video)


