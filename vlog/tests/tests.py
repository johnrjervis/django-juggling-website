from django.test import TestCase
from django.urls import resolve
from django.utils import timezone
from vlog.models import JugglingVideo
from datetime import timedelta

class IndexViewTest(TestCase):

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/juggling/')

        self.assertTemplateUsed(response, 'vlog/index.html')

    def test_home_page_displays_error_if_no_videos_in_database(self):
        response = self.client.get('/juggling/')

        self.assertContains(response, 'No videos are available!')

    def test_home_page_hides_video_element_if_no_videos_available(self):
        response = self.client.get('/juggling/')

        self.assertNotContains(response, '</video>')

    def test_home_page_hides_error_if_videos_are_available(self):
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response = self.client.get('/juggling/')

        self.assertNotContains(response, 'No videos are available!')

    def test_home_page_shows_video_if_availabe(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get('/juggling/')

        self.assertContains(response, first_video.filename)

    def test_home_page_shows_most_recently_published_video(self):
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        older_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = older_date)
        current_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = current_date)

        response = self.client.get('/juggling/')

        self.assertContains(response, current_video.filename)
        self.assertNotContains(response, older_video.filename)

    def test_home_page_does_not_show_videos_that_have_a_publication_date_in_the_future(self):
        """
        Videos with a publication date in the future should not appear on the homepage
        """
        future_date = timezone.now() + timedelta(days = 5)
        current_date = timezone.now()
        future_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = future_date)
        current_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = current_date)

        response = self.client.get('/juggling/')

        self.assertContains(response, current_video.filename)
        self.assertNotContains(response, future_video.filename)

class VideoDetailViewTest(TestCase):

    def test_detail_view_uses_correct_template(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(f'/juggling/videos/{first_video.id}/')

        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_detail_view_displays_video(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(f'/juggling/videos/{first_video.id}/')

        self.assertContains(response, first_video.filename)

    def test_detail_views_only_display_correct_videos(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')
        second_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response1 = self.client.get(f'/juggling/videos/{first_video.id}/')
        response2 = self.client.get(f'/juggling/videos/{second_video.id}/')

        self.assertContains(response1, first_video.filename)
        self.assertNotContains(response1, second_video.filename)
        self.assertContains(response2, second_video.filename)
        self.assertNotContains(response2, first_video.filename)

    def test_detail_view_displays_title(self):
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', title = 'Five ball juggle 50 catches')

        response = self.client.get(f'/juggling/videos/{first_video.id}/')

        self.assertContains(response, first_video.title)

    def test_detail_view_displays_pub_date(self):
        pub_time = timezone.now()
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = pub_time)

        response = self.client.get(f'/juggling/videos/{first_video.id}/')
        time_string = pub_time.strftime(format = '%Y/%m/%d at %H:%M')
        #print(response.content.decode())

        self.assertContains(response, time_string)

    def test_detail_view_unavailable_for_videos_with_a_pub_date_in_the_future(self):
        """
        The URL for a video object with a publication date in the future should respond with a 404 error
        """
        future_date = timezone.now() + timedelta(days = 5)
        future_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = future_date)

        response = self.client.get(f'/juggling/videos/{future_video.id}/')

        self.assertEqual(response.status_code, 404)


class VideosListViewTest(TestCase):

    def test_video_list_view_uses_correct_template(self):
        response = self.client.get('/juggling/videos/')

        self.assertTemplateUsed(response, 'vlog/videos.html')

    def test_older_video_displayed_in_videos_archive(self):
        """
        The homepage displays the most recently published article
        All other videos should be displayed on the videos page (the archive)
        """
        older_date = timezone.now() - timedelta(days = 5)
        newer_date = timezone.now()
        older_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = older_date)
        newer_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = newer_date)

        response = self.client.get('/juggling/videos/')

        self.assertContains(response, older_video.filename)
        self.assertNotContains(response, newer_video.filename)

    def test_videos_delivered_in_order_of_increasing_age_in_context(self):
        """
        Videos in the archive should be provided to the HTML in increasing age oder so that newer videos appear first on the page
        """
        oldest_date = timezone.now() - timedelta(days = 10)
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        oldest_video = JugglingVideo.objects.create(filename = 'under_the_arm.mp4', pub_date = oldest_date)
        older_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = older_date)
        current_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = current_date)

        response = self.client.get('/juggling/videos/')

        self.assertEqual(len(response.context['videos_list']), 2)
        self.assertEqual(response.context['videos_list'][0], older_video)
        self.assertEqual(response.context['videos_list'][1], oldest_video)

    def test_videos_page_displays_multiple_videos(self):
        """
        The archive should display all videos published before the latest video
        """
        oldest_date = timezone.now() - timedelta(days = 10)
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        oldest_video = JugglingVideo.objects.create(filename = 'under_the_arm.mp4', pub_date = oldest_date)
        older_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = older_date)
        current_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = current_date)

        response = self.client.get('/juggling/videos/')

        self.assertContains(response, older_video.filename)
        self.assertContains(response, oldest_video.filename)

    def test_videos_page_not_affected_by_videos_with_a_publication_date_in_the_future(self):
        """
        The videos page should ignore videos with a publication date in the future
        Of the rest of the videos, the most recent (non-future) video should appear on the home page
        The rest should appear on the videos page
        """
        future_date = timezone.now() + timedelta(days = 5)
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        future_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = future_date)
        older_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = older_date)
        current_video = JugglingVideo.objects.create(filename = 'under_the_arm.mp4', pub_date = current_date)

        response = self.client.get('/juggling/videos/')

        self.assertContains(response, older_video.filename)
        self.assertNotContains(response, current_video.filename)
        self.assertNotContains(response, future_video.filename)

class VideoModelTest(TestCase):

    def test_saving_and_retrieving_videos(self):
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', title = 'Behind the back juggle', pub_date = timezone.now())

        saved_videos = JugglingVideo.objects.all()
        first_saved_video = saved_videos[0]

        self.assertEqual(saved_videos.count(), 1)
        self.assertEqual(first_video.filename, first_saved_video.filename)
        self.assertEqual(first_video.title, first_saved_video.title)
        self.assertEqual(first_video.pub_date, first_saved_video.pub_date)
