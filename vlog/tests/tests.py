from django.test import TestCase
from django.urls import resolve
from vlog.models import JugglingVideo

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')


class VideoModelTest(TestCase):

    def test_home_page_displays_error_if_no_videos_in_database(self):
        response = self.client.get('/')
        self.assertIn('No videos are available!', response.content.decode())

    def test_saving_and_retrieving_videos(self):
        first_video = JugglingVideo()
        first_video.filename = 'behind_the_back_juggle.mp4'
        first_video.save()

        saved_videos = JugglingVideo.objects.all()
        self.assertEqual(saved_videos.count(), 1)

        first_saved_video = saved_videos[0]
        self.assertEqual(first_video.filename, first_saved_video.filename)
