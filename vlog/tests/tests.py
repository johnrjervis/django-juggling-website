from django.test import TestCase
from django.urls import resolve
from vlog.models import JugglingVideo

class HomePageViewTest(TestCase):

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'vlog/index.html')

    def test_home_page_displays_error_if_no_videos_in_database(self):
        response = self.client.get('/')

        self.assertContains(response, 'No videos are available!')

    def test_home_page_hides_video_element_if_no_videos_available(self):
        response = self.client.get('/')

        self.assertNotContains(response, '</video>')

    def test_home_page_hides_error_if_videos_are_available(self):
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response = self.client.get('/')

        self.assertNotContains(response, 'No videos are available!')

    def test_home_page_shows_video_if_availabe(self):
        first_video = JugglingVideo()
        first_video.filename = 'five_ball_juggle_50_catches.mp4'
        first_video.save()

        response = self.client.get('/')
        #print(response.content.decode())

        self.assertContains(response, first_video.filename)

class VideoDetailViewTest(TestCase):

    def test_detail_view_uses_correct_template(self):
        response = self.client.get('/videos/1/')

        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_detail_view_displays_video(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get('/videos/1/')

        self.assertContains(response, first_video.filename)

class VideoModelTest(TestCase):

    def test_saving_and_retrieving_videos(self):
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
