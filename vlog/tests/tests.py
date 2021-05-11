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

    def test_home_page_hides_video_element_if_no_videos_available(self):
        response = self.client.get('/')

        self.assertNotIn('</video>', response.content.decode())

    def test_home_page_hides_error_if_videos_are_available(self):
        first_video = JugglingVideo()
        first_video.filename = 'behind_the_back_juggle.mp4'
        first_video.save()

        response = self.client.get('/')

        self.assertNotIn('No videos are available!', response.content.decode())

    def test_home_page_shows_video_if_availabe(self):
        first_video = JugglingVideo()
        first_video.filename = 'five_ball_juggle_50_catches.mp4'
        first_video.save()

        response = self.client.get('/')
        #print(response.content.decode())

        self.assertIn(first_video.filename, response.content.decode())

    def test_saving_and_retrieving_videos(self):
        first_video = JugglingVideo()
        first_video.filename = 'behind_the_back_juggle.mp4'
        first_video.save()

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
