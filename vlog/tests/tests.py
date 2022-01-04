from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from vlog.models import JugglingVideo
from datetime import timedelta

class JugglingVideoSiteTest(TestCase):

    def check_context_dict_contains_correct_selected_item_for_view(self, view_name, desired_selected_value, arguments = None):
        """
        The context dict for a given view should contain the correct value for 'selected' in the context dict
        The selected class should appear on the appropriate page
        """
        # Note the name of this method cannot include test, because it is not intended to be run 'as is'
        # Create a test method in a sub-class and call this method from that test
        response = self.client.get(reverse(view_name, args = arguments))
        selected = response.context[-1].get('selected')

        self.assertEqual(selected, desired_selected_value)
        self.assertContains(response, '<li class="navlink selected">')


class IndexViewTest(JugglingVideoSiteTest):
    """
    Tests for the index (AKA the home page)
    """

    def test_home_page_uses_correct_template(self):
        """
        The correct template should be used when the home page is accessed 
        """
        response = self.client.get(reverse('vlog:index'))

        self.assertTemplateUsed(response, 'vlog/index.html')

    def test_home_page_displays_error_if_no_videos_in_database(self):
        """
        The home page should display an error message if there are no video objects in the database 
        """
        response = self.client.get(reverse('vlog:index'))

        self.assertContains(response, 'No videos are available!')

    def test_home_page_hides_video_element_if_no_videos_available(self):
        """
        The home page should not display any video elements if there are no video objects in the database 
        """
        response = self.client.get(reverse('vlog:index'))

        self.assertNotContains(response, '</video>')

    def test_home_page_hides_error_if_videos_are_available(self):
        """
        The home page should not display an error message if there is a video object in the database 
        """
        first_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response = self.client.get(reverse('vlog:index'))

        self.assertNotContains(response, 'No videos are available!')

    def test_home_page_shows_video_if_availabe(self):
        """
        The home page should display a video if there is a video object in the database 
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(reverse('vlog:index'))

        self.assertContains(response, first_video.filename)

    def test_home_page_shows_most_recently_published_video(self):
        """
        The home page should only display the video with the most recent publication date 
        """
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        older_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4', pub_date = older_date)
        current_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = current_date)

        response = self.client.get(reverse('vlog:index'))

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

        response = self.client.get(reverse('vlog:index'))

        self.assertContains(response, current_video.filename)
        self.assertNotContains(response, future_video.filename)

    def test_context_dict_contains_correct_selected_item_for_index_view(self):
        """
        The context dict for the home page view should contain 'selected': 'Home'
        The selected class should appear on the home page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:index', 'Home')


class VideoDetailViewTest(JugglingVideoSiteTest):
    """
    Tests for the video detail view pages
    """

    def test_detail_view_uses_correct_template(self):
        """
        The correct template should be used when a video's detail page is accessed 
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_detail_view_displays_video(self):
        """
        The detail page for a juggling video object should display the correct video
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertContains(response, first_video.filename)

    def test_detail_views_only_display_correct_videos(self):
        """
        The detail page for a juggling video object should only display the correct video
        (Other videos in the database should not be displayed)
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4')
        second_video = JugglingVideo.objects.create(filename = 'behind_the_back_juggle.mp4')

        response1 = self.client.get(reverse('vlog:detail', args = [first_video.id]))
        response2 = self.client.get(reverse('vlog:detail', args = [second_video.id]))

        self.assertContains(response1, first_video.filename)
        self.assertNotContains(response1, second_video.filename)
        self.assertContains(response2, second_video.filename)
        self.assertNotContains(response2, first_video.filename)

    def test_detail_view_displays_title(self):
        """
        A video's title attribute should be displayed on the video's detail page
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', title = 'Five ball juggle 50 catches')

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertContains(response, first_video.title)

    def test_detail_view_displays_pub_date(self):
        """
        A video's publication date attribute should be displayed on the video's detail page
        """
        pub_time = timezone.now()
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = pub_time)

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))
        time_string = pub_time.strftime(format = '%Y/%m/%d at %H:%M')
        #print(response.content.decode())

        self.assertContains(response, time_string)

    def test_detail_view_unavailable_for_videos_with_a_pub_date_in_the_future(self):
        """
        The URL for a video object with a publication date in the future should respond with a 404 error
        """
        future_date = timezone.now() + timedelta(days = 5)
        future_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = future_date)

        response = self.client.get(reverse('vlog:detail', args = [future_video.id]))

        self.assertEqual(response.status_code, 404)

    def test_context_dict_contains_correct_selected_item_for_video_detail_view(self):
        """
        The context dict for the video detail view should contain 'selected': 'Videos'
        The selected class should appear on the video page
        """
        pub_time = timezone.now()
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', pub_date = pub_time)

        self.check_context_dict_contains_correct_selected_item_for_view('vlog:detail', 'Videos', arguments = [first_video.id])

    def test_detail_view_can_save_a_POST_request(self):
        """
        Test that comments posted to a video are saved to the detail page
        """
        first_video = JugglingVideo.objects.create(filename = 'five_ball_juggle_50_catches.mp4', title = 'Five ball juggle 50 catches')

        response = self.client.post(reverse('vlog:detail', args = [first_video.id]), data = {'comment_text': 'Nice video!'})

        self.assertContains(response, 'Nice video!')
        self.assertTemplateUsed(response, 'vlog/detail.html')


class VideosListViewTest(JugglingVideoSiteTest):
    """
    Tests for the videos page (AKA the archive)
    """

    def test_video_list_view_uses_correct_template(self):
        """
        The correct template should be used when the videos archive page is accessed 
        """
        response = self.client.get(reverse('vlog:videos'))

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

        response = self.client.get(reverse('vlog:videos'))

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

        response = self.client.get(reverse('vlog:videos'))

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

        response = self.client.get(reverse('vlog:videos'))

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

        response = self.client.get(reverse('vlog:videos'))

        self.assertContains(response, older_video.filename)
        self.assertNotContains(response, current_video.filename)
        self.assertNotContains(response, future_video.filename)

    def test_context_dict_contains_correct_selected_item_for_videos_list_view(self):
        """
        The context dict for the video list view should contain 'selected': 'Videos'
        The selected class should appear on the video page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:videos', 'Videos')


class LearnViewTest(JugglingVideoSiteTest):
    """
    Tests for the Learn page
    """

    def test_learn_view_uses_correct_template(self):
        """
        Test that this view uses the correct template
        """
        response = self.client.get(reverse('vlog:learn'))

        self.assertTemplateUsed(response, 'vlog/learn.html')

    def test_learn_page_under_construction(self):
        """
        Test that the Learn page displays a message that explains it has not yet been built
        """
        response = self.client.get(reverse('vlog:learn'))

        self.assertContains(response, 'This part of the site is still under construction.')

    def test_context_dict_contains_correct_selected_item_for_learn_view(self):
        """
        The context dict for the learn view should contain 'selected': 'Learn'
        The selected class should appear on the Learn page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:learn', 'Learn')


class AboutViewTest(JugglingVideoSiteTest):
    """
    Tests for the About page
    """

    def test_about_view_uses_correct_template(self):
        """
        Test that this view uses the correct template
        """
        response = self.client.get(reverse('vlog:about'))

        self.assertTemplateUsed(response, 'vlog/about.html')

    def test_about_page_links_to_info_pages(self):
        """
        Test that the About page links to pages that provide extra information about the site
        """
        response = self.client.get(reverse('vlog:about'))

        self.assertContains(response, reverse('vlog:thanks'))
        self.assertContains(response, reverse('vlog:history'))

    def test_context_dict_contains_correct_selected_item_for_about_view(self):
        """
        The context dict for the about view should contain 'selected': 'About'
        The selected class should appear on the About page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:about', 'About')


class ThanksViewTest(JugglingVideoSiteTest):
    """
    Tests for the Acknowledgements page
    """

    def test_thanks_view_uses_correct_template(self):
        """
        Test that this view uses the correct template
        """
        response = self.client.get(reverse('vlog:thanks'))

        self.assertTemplateUsed(response, 'vlog/thanks.html')

    def test_thanks_page_links_to_external_pages(self):
        """
        Test that the Thanks page links to external pages
        """
        response = self.client.get(reverse('vlog:thanks'))

        self.assertContains(response, 'https://www.')

    def test_context_dict_contains_correct_selected_item_for_thanks_view(self):
        """
        The context dict for the thanks view should contain 'selected': 'About' (it's in the 'About' section)
        The selected class should appear on the Thanks page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:thanks', 'About')


class HistoryViewTest(JugglingVideoSiteTest):
    """
    Tests for the History page
    """

    def test_history_view_uses_correct_template(self):
        """
        Test that this view uses the correct template
        """
        response = self.client.get(reverse('vlog:history'))

        self.assertTemplateUsed(response, 'vlog/history.html')

    def test_history_page_shows_site_info(self):
        """
        Test that the History page provides some information about the site's history
        """
        response = self.client.get(reverse('vlog:history'))

        self.assertContains(response, 'The history of this site')

    def test_context_dict_contains_correct_selected_item_for_history_view(self):
        """
        The context dict for the history view should contain 'selected': 'About' (it's in the 'About' section)
        The selected class should appear on the History page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('vlog:history', 'About')


class VideoModelTest(TestCase):
    """
    Tests for the database)
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

