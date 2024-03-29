from os import environ as os_environ
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import vlog.views
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from vlog.forms import CommentForm, EMPTY_COMMENT_ERROR, DUPLICATE_COMMENT_ERROR
from datetime import timedelta
from .base import JugglingVideoSiteTest

from unittest import skip
from unittest.mock import patch

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

    def test_root_url_redirects_to_homepage(self):
        """
        Test that a request to the root URL redirects to the homepage
        """
        response = self.client.get('/')

        self.assertRedirects(response, reverse('vlog:index'))

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
        self.post_video()

        response = self.client.get(reverse('vlog:index'))

        self.assertNotContains(response, 'No videos are available!')

    def test_home_page_shows_video_if_available(self):
        """
        The home page should display a video if there is a video object in the database 
        """
        first_video = self.post_video()

        response = self.client.get(reverse('vlog:index'))

        self.assertContains(response, f'vlog/videos/{first_video.filename}')

    def test_home_page_shows_most_recently_published_video(self):
        """
        The home page should only display the video with the most recent publication date 
        """
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        older_video = self.post_video(video = 'first', pub_date = older_date)
        current_video = self.post_video(video = 'second', pub_date = current_date)

        response = self.client.get(reverse('vlog:index'))

        self.assertContains(response, current_video.filename)
        self.assertNotContains(response, older_video.filename)

    def test_home_page_does_not_show_videos_that_have_a_publication_date_in_the_future(self):
        """
        Videos with a publication date in the future should not appear on the homepage
        """
        current_date = timezone.now()
        future_date = timezone.now() + timedelta(days = 5)
        current_video = self.post_video(video = 'first', pub_date = current_date)
        future_video = self.post_video(video = 'second', pub_date = future_date)

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
        first_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_video_detail_view_passes_correct_video_to_template(self):
        """
        Tests that the video detail view passes the correct view in the context dictionary
        """
        correct_video = self.post_video(video = 'first')
        other_video = self.post_video(video = 'second')

        response = self.client.get(reverse('vlog:detail', args = [correct_video.id]))

        self.assertEqual(response.context['video'], correct_video)

    def test_detail_view_displays_video(self):
        """
        The detail page for a juggling video object should display the correct video
        """
        first_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertContains(response, f'vlog/videos/{first_video.filename}')

    def test_detail_views_only_display_correct_videos(self):
        """
        The detail page for a juggling video object should only display the correct video
        (Other videos in the database should not be displayed)
        """
        first_video = self.post_video(video = 'first')
        second_video = self.post_video(video = 'second')

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
        first_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertContains(response, first_video.title)

    def test_detail_view_displays_pub_date(self):
        """
        A video's publication date attribute should be displayed on the video's detail page
        """
        current_time = timezone.now()
        first_video = self.post_video(video = 'first', pub_date = current_time)

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))
        time_string = current_time.strftime(format = '%d/%m/%Y at %H:%M')
        #print(response.content.decode())

        self.assertContains(response, time_string)

    def test_detail_view_unavailable_for_videos_with_a_pub_date_in_the_future(self):
        """
        The URL for a video object with a publication date in the future should respond with a 404 error
        """
        future_date = timezone.now() + timedelta(days = 5)
        future_video = self.post_video(pub_date = future_date)

        response = self.client.get(reverse('vlog:detail', args = [future_video.id]))

        self.assertEqual(response.status_code, 404)

    def test_context_dict_contains_correct_selected_item_for_video_detail_view(self):
        """
        The context dict for the video detail view should contain 'selected': 'Videos'
        The selected class should appear on the video page
        """
        pub_time = timezone.now()
        first_video = self.post_video(pub_date = pub_time)

        self.check_context_dict_contains_correct_selected_item_for_view('vlog:detail', 'Videos', arguments = [first_video.id])

    def test_video_detail_view_only_saves_items_when_required(self):
        """
        Tests that the video detail view does not save blank comments when the page is visited
        """
        first_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [first_video.id]))

        self.assertEqual(VideoComment.objects.count(), 0)

    def test_video_detail_view_only_displays_comments_for_the_correct_video(self):
        """
        Test that the video detail view only displays comments that relate to the specified video
        """
        correct_video = self.post_video(video = 'first')
        VideoComment.objects.create(text = 'First comment!', video = correct_video)
        VideoComment.objects.create(text = 'Nice video!', video = correct_video)
        other_video = self.post_video(video = 'second')
        VideoComment.objects.create(text = 'Other video comment #1', video = other_video)
        VideoComment.objects.create(text = 'Other video comment #2', video = other_video)

        response = self.client.get(reverse('vlog:detail', args = [correct_video.id]))

        self.assertContains(response, 'First comment!')
        self.assertContains(response, 'Nice video!')
        self.assertNotContains(response, 'Other comment #1')
        self.assertNotContains(response, 'Other comment #2')

    def test_video_detail_view_displays_poster_as_anonymous_if_no_name_supplied(self):
        """
        If no name is entered, the comment should include 'anonymous'
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', video = juggling_video)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'First comment!')
        self.assertContains(response, 'Posted by anonymous')


    def test_video_detail_view_displays_comment_poster_name_if_supplied(self):
        """
        If a name is supplied for a comment then it should be displayed with the comment'
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', author = 'A juggling fan', video = juggling_video)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'First comment!')
        self.assertContains(response, 'Posted by A juggling fan')

    def test_video_detail_view_displays_comment_date(self):
        """
        Tests that the date and time that a comment was posted appear alongside the comment text
        """
        # Give the video an arbitrary pub date in the past so that this does not match the comment's date
        video_pub_date = timezone.now() - timedelta(days = 7, hours = 4, minutes = 30)
        comment_post_date = timezone.now()
        juggling_video = self.post_video(pub_date = video_pub_date)
        VideoComment.objects.create(text = 'First comment!', author = 'A juggling fan', video = juggling_video, date = comment_post_date)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))
        date_string = comment_post_date.strftime(format = '%d/%m/%Y at %H:%M')

        self.assertContains(response, 'First comment!')
        self.assertContains(response, date_string)

    def test_video_detail_view_only_displays_approved_comments(self):
        """
        Comments should only appear on a video's detail page if their is_approved attribute is True
        """
        # Give the video an arbitrary pub date in the past so that this does not match the comment's date
        juggling_video = self.post_video()
        approved_comment = VideoComment.objects.create(text = 'First comment!', video = juggling_video, is_approved = True)
        not_approved_comment = VideoComment.objects.create(text = 'Inappropriate comment', video = juggling_video, is_approved = False)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'First comment!')
        self.assertNotContains(response, 'Inappropriate comment')

    def test_can_save_a_comment_from_a_POST_request_for_an_existing_video(self):
        """
        Test that a POST request from the video detail page saves the comment to the database
        """
        correct_video = self.post_video(video = 'first')
        other_video = self.post_video(video = 'second')

        response = self.post_comment(video = correct_video, text = 'First comment on correct video!')
        first_comment = VideoComment.objects.first()

        self.assertEqual(VideoComment.objects.count(), 1)
        self.assertEqual(first_comment.text, 'First comment on correct video!')
        self.assertEqual(first_comment.video, correct_video)

    def test_new_comment_POST_redirects_back_to_video_detail_page(self):
        """
        Test that when a comment is posted for a video, the browser is redirected to the detail page for that video
        """
        correct_video = self.post_video(video = 'first')
        other_video = self.post_video(video = 'second')

        response = self.post_comment(video = correct_video, text = 'First comment on correct video!')

        self.assertRedirects(response, reverse('vlog:detail', args = [correct_video.id]))

    def test_comment_POST_can_save_the_comment_authors_name(self):
        """
        Test that a comment author's name is saved to the database
        """
        juggling_video = self.post_video()

        response = self.post_comment(video = juggling_video, text = 'First comment!', author = 'A juggling fan')
        comment = VideoComment.objects.first()

        self.assertEqual(comment.text, 'First comment!')
        self.assertEqual(comment.author, 'A juggling fan')

    def test_comment_author_is_anonymous_if_POST_does_not_include_name(self):
        """
        Test that a comment author's name is saved as anonymous if no name is supplied
        """
        juggling_video = self.post_video()

        response = self.post_comment(video = juggling_video, text = 'First comment!')
        comment = VideoComment.objects.first()

        self.assertEqual(comment.text, 'First comment!')
        self.assertEqual(comment.author, 'anonymous')

    def test_comment_invite_is_displayed_if_video_has_no_comments(self):
        """
        Test that an invite is shown if no comments have been posted
        """
        juggling_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'There are no comments for this video yet. Use the form below to post the first comment!')

    def test_comment_invite_is_displayed_if_video_has_no_approved_comments(self):
        """
        Test that an invite is shown if all the comments posted for the video are not approved
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', video = juggling_video, is_approved = False)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'There are no comments for this video yet. Use the form below to post the first comment!')

    def test_comment_invite_is_not_displayed_if_a_comment_has_been_posted_for_a_video(self):
        """
        Test that the invite is not shown if a comment has been posted
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', video = juggling_video)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertNotContains(response, 'There are no comments for this video yet. Use the form below to post the first comment!')

    def test_author_comment_is_displayed_in_video_detail_view(self):
        """
        Test that comments by the video author (JJ) are displayed in the video detail view
        """
        juggling_video = self.post_video()
        VideoComment.objects.create(text = 'First comment!', video = juggling_video)

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertContains(response, 'This is the video that started it all!')

    def test_invalid_form_is_rendered_with_the_detail_template(self):
        """
        Test that if a blank comment is posted, the response is directed back to the detail view
        """
        juggling_video = self.post_video()

        response = self.post_comment(juggling_video, text = '', author = '')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vlog/detail.html')

    def test_comment_form_passed_to_template_after_invalid_input(self):
        """
        Test that the comment form is passed to the detail template if an empty comment is submitted
        """
        juggling_video = self.post_video()

        response = self.post_comment(juggling_video, text = '', author = '')

        self.assertIsInstance(response.context['form'], CommentForm)

    def test_empty_comments_are_not_saved(self):
        """
        Test that a comment is not saved to the database if it is empty
        """
        juggling_video = self.post_video()

        response = self.post_comment(juggling_video, text = '', author = '')

        self.assertEqual(VideoComment.objects.count(), 0)

    def test_detail_view_has_comment_form(self):
        """
        A CommentForm object should be in the context dict of the detail view (under the key 'form')
        """
        juggling_video = self.post_video()

        response = self.client.get(reverse('vlog:detail', args = [juggling_video.id]))

        self.assertIsInstance(response.context['form'], CommentForm)

    def test_duplicate_comment_validation_errors_are_displayed_on_video_detail_page(self):
        """
        An error message should be displayed on the video detail page if a comment is duplicated
        """
        juggling_video = self.post_video()
        video_comment = VideoComment.objects.create(text = 'comment text', video = juggling_video)

        response = self.post_comment(juggling_video, text = 'comment text', author = '')
        expected_error = DUPLICATE_COMMENT_ERROR

        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'vlog/detail.html')
        self.assertEqual(VideoComment.objects.all().count(), 1)


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
        older_video = self.post_video(video = 'first', pub_date = older_date)
        newer_video = self.post_video(video = 'second', pub_date = newer_date)

        response = self.client.get(reverse('vlog:videos'))

        self.assertContains(response, f'vlog/videos/{older_video.filename}')
        self.assertNotContains(response, newer_video.filename)

    def test_videos_delivered_in_order_of_increasing_age_in_context(self):
        """
        Videos in the archive should be provided to the HTML in increasing age oder so that newer videos appear first on the page
        """
        oldest_date = timezone.now() - timedelta(days = 10)
        older_date = timezone.now() - timedelta(days = 5)
        current_date = timezone.now()
        oldest_video = self.post_video(video = 'first', pub_date = oldest_date)
        older_video = self.post_video(video = 'second', pub_date = older_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

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
        oldest_video = self.post_video(video = 'first', pub_date = oldest_date)
        older_video = self.post_video(video = 'second', pub_date = older_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

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
        future_video = self.post_video(video = 'first', pub_date = future_date)
        older_video = self.post_video(video = 'second', pub_date = older_date)
        current_video = self.post_video(video = 'third', pub_date = current_date)

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
        first_acknowledgement = Acknowledgement.objects.create(name ='Django', link ='https://www.djangoproject.com/', description = 'This site was built using the Django framework.')

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

@patch('vlog.views.send_mail')
class ContactViewTest(JugglingVideoSiteTest):
    """
    Tests for the Contact page
    """

    def test_contact_view_uses_correct_template(self, mock_send_mail):
        """
        Test that this view uses the correct template
        """
        response = self.client.get(reverse('vlog:contact'))

        self.assertTemplateUsed(response, 'vlog/contact.html')

    def test_contact_post_redirects_to_contact_page(self, mock_send_mail):
        """
        Test that the page redirects to the contact form after the form is submitted
        """
        response = self.client.post(reverse('vlog:contact'), data = {
            'message': 'Great website!',
            'sender_name': 'Anonymous',
        })

        self.assertRedirects(response, reverse('vlog:contact'))

    def test_contact_post_sends_email(self, mock_send_mail):
        """
        Uses mocks to check that a POST request to the contact form calls send_mail in the correct manner
        """
        self.client.post(reverse('vlog:contact'), data = {
            'message': 'Love the website!',
            'sender_name': 'Anonymous',
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "A message from a website visitor")
        self.assertEqual(from_email, os_environ.get('OUTBOUND_EMAIL_ADDRESS'))
        self.assertEqual(to_list, [os_environ.get('EMAIL_ADDRESS')])

    def test_contact_post_includes_form_data_in_email(self, mock_send_mail):
        """
        The contact form's sender and message fields should be included in the body of the email that is sent
        """
        self.client.post(reverse('vlog:contact'), data = {
            'sender_name': 'A juggling fan',
            'message': 'Great website!',
        })

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn('From: A juggling fan', body)
        self.assertIn('Message: Great website!', body)

    def test_contact_form_submission_adds_success_message(self, mock_send_mail):
        """
        A success message should be displayed when the contact form is submitted
        """
        response = self.client.post(reverse('vlog:contact'), data={
            'message': 'meh',
            'sender_name': 'Anonymous',
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 'Your message has been sent!')
        self.assertEqual(message.tags, 'success')

    def test_contact_form_submission_without_message_adds_warning_message(self, mock_send_mail):
        """
        A warning message should be displayed when the contact form is submitted with a blank message field
        """
        response = self.client.post(reverse('vlog:contact'), data={
            'message': '',
            'sender_name': 'Anonymous',
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 'Please enter a message.')
        self.assertEqual(message.tags, 'warning')

    def test_contact_post_without_message_does_not_send_email(self, mock_send_mail):
        """
        Uses mocks to check that a POST request to the contact form without a message property does not call send_mail
        """
        self.client.post(reverse('vlog:contact'), data = {
            'message': '',
            'sender_name': 'Anonymous',
        })

        self.assertFalse(mock_send_mail.called)

