from django.test import TestCase
from django.urls import resolve
from django.utils import timezone
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

        self.assertContains(response, first_video.filename)

class VideoDetailViewTest(TestCase):

    def test_detail_view_uses_correct_template(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(f'/videos/{first_video.id}/')

        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_detail_view_displays_video(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(f'/videos/{first_video.id}/')

        self.assertContains(response, first_video.filename)

    def test_detail_views_only_display_correct_videos(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')
        second_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response1 = self.client.get(f'/videos/{first_video.id}/')
        response2 = self.client.get(f'/videos/{second_video.id}/')

        self.assertContains(response1, first_video.filename)
        self.assertNotContains(response1, second_video.filename)
        self.assertContains(response2, second_video.filename)
        self.assertNotContains(response2, first_video.filename)

    def test_detail_view_displays_title(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', title = 'Five ball juggle 50 catches')

        response = self.client.get(f'/videos/{first_video.id}/')

        self.assertContains(response, first_video.title)

    def test_detail_view_displays_pub_date(self):
        pub_time = timezone.now()
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = pub_time)

        response = self.client.get(f'/videos/{first_video.id}/')
        time_string = pub_time.strftime(format = '%Y/%m/%d at %H:%M')
        #print(response.content.decode())

        self.assertContains(response, time_string)

class VideoModelTest(TestCase):

    def test_saving_and_retrieving_videos(self):
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle', pub_date = timezone.now())

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
        self.assertEqual(first_video.title, first_saved_video.title)
        self.assertEqual(first_video.pub_date, first_saved_video.pub_date)
