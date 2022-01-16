from .base import AdminAndSiteVisitorTest
from django.utils import timezone
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime as dt


class T02VideoArchiveAndDetailViewTest(AdminAndSiteVisitorTest):

    def check_for_comment_in_comments_section(self, comment_text):
        comments_section = self.wait_for(lambda: self.browser.find_element_by_class_name('comments'))
        comments = comments_section.find_elements_by_class_name('comment')

        self.assertIn(comment_text, [comment.text for comment in comments])

    def datestring_to_datetime(self, datestring):
        """Converts the pub date (as it appears on the page) into a datetime object"""
        date, time = datestring.strip('Published on ').split(' at ')
        year, month, day = date.split('/')
        hours, minutes = time.split(':')
        datelist = [int(elem) for elem in [year, month, day, hours, minutes]]
        return dt.datetime(*datelist, tzinfo = dt.timezone.utc)

    def test_detail_views_and_video_archive(self):

        # JJ has already uploaded a couple of videos to the site
        self.jj_browser.get(f'{self.live_server_url}/admin/')
        username_field = self.jj_browser.find_element_by_id('id_username')
        username_field.send_keys('admin_user')
        password_field = self.jj_browser.find_element_by_id('id_password')
        password_field.send_keys('secret_password')
        password_field.send_keys(Keys.ENTER)
        application_div = self.wait_for(lambda: self.jj_browser.find_element_by_class_name('app-vlog'))
        #self.assertIn('Juggling videos', application_div.text)
        add_video_link = application_div.find_element_by_link_text('Add')
        add_video_link.click()
        new_video_field = self.wait_for(lambda: self.jj_browser.find_element_by_id('id_filename'))
        ## Need to find a way to send times to the date field in the admin site if I want to adjust pub dates
        first_pub_date = timezone.now()
        first_video_filename = 'five_ball_juggle_50_catches.mp4'
        new_video_field.send_keys(first_video_filename)
        title_field = self.jj_browser.find_element_by_id('id_title')
        first_video_title = 'Five ball juggle 50 catches'
        title_field.send_keys(first_video_title)
        title_field.send_keys(Keys.ENTER)
        add_new_video_link = self.wait_for(lambda: self.jj_browser.find_element_by_link_text('ADD JUGGLING VIDEO'))
        add_new_video_link.click()
        new_video_field = self.wait_for(lambda: self.jj_browser.find_element_by_id('id_filename'))
        # A second video was added just now
        second_pub_date = timezone.now()
        self.assertGreaterEqual(second_pub_date, first_pub_date)
        second_video_filename = 'behind_the_back_juggle.mp4'
        new_video_field.send_keys(second_video_filename)
        title_field = self.jj_browser.find_element_by_id('id_title')
        second_video_title = 'Behind the back juggle'
        title_field.send_keys(second_video_title)
        title_field.send_keys(Keys.ENTER)

        # A site visitor goes to the homepage
        self.browser.get(f'{self.live_server_url}/juggling/')

        # The visitor notices that there is a link for commenting on the video
        video_comment_link = self.wait_for(lambda: self.browser.find_element_by_class_name('comment_link'))
        self.assertIn('Comment on this video', video_comment_link.text)
        # The user clicks the link
        video_comment_link.click()
        # The title of the video is displayed
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_class_name('detail_heading').text, second_video_title))
        # The video's publication date is also displayed
        displayed_date_field = self.browser.find_element_by_class_name('video_pub_date')
        displayed_pub_date = self.datestring_to_datetime(displayed_date_field.text)
        #self.assertIn(first_pub_date, displayed_date.text) # Replaced by assertAlmostEqual statement below
        self.assertAlmostEqual(second_pub_date, displayed_pub_date, delta = dt.timedelta(seconds = 65))
        # The format of the further info link is the base url + videos/ + a number with at least one digit
        self.assertRegex(self.browser.current_url, r'/videos/\d+')

        # The visitor sees an input field for posting comments
        comment_field = self.browser.find_element_by_tag_name('textarea')
        self.assertEqual(comment_field.get_attribute('placeholder'), 'Enter a comment')
        # The visitor enters a comment and clicks the 'Post comment' button
        comment_field.send_keys('First post!')
        submit_button = self.browser.find_element_by_tag_name('button')
        submit_button.click()
        # The comment appears on the page
        self.check_for_comment_in_comments_section('First post!')
        # The visitor then accidentally clicks the submit button while the comment field is empty
        #submit_button = self.browser.find_element_by_tag_name('button')
        #submit_button.click()
        # The page refreshes and displays a warning to say that the blank comment could not be submitted
        #self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_class_name('comment_warning').text, 'Could not submit blank comment'))

        # Intrigued to see what other videos are available, the visitor clicks the archive link
        video_archive_link = self.browser.find_element_by_link_text('Videos')
        video_archive_link.click()
        # The first video posted to the site is in the archive
        self.wait_for(lambda: self.assertIn(first_video_filename, self.browser.find_element_by_tag_name('video').get_attribute('innerHTML')))
        # This is the only video in the archive, as the video on the home page has not been moved to the archive yet 
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 1)
        self.assertNotIn(second_video_filename, videos[0].get_attribute('innerHTML'))

        # Once again, there is a link for comments
        archive_video_comment_link = self.wait_for(lambda: self.browser.find_element_by_class_name('comment_link'))
        # The user clicks the link
        archive_video_comment_link.click()
        # The title of this video is displayed
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_class_name('detail_heading').text, first_video_title))
        # The video's publication date is also displayed - it is about a week old
        older_displayed_date_field = self.browser.find_element_by_class_name('video_pub_date')
        older_displayed_pub_date = self.datestring_to_datetime(older_displayed_date_field.text)
        self.assertAlmostEqual(first_pub_date, older_displayed_pub_date, delta = dt.timedelta(seconds = 65))

        # The user enters a comment for this video
        comment_field = self.browser.find_element_by_tag_name('textarea')
        comment_field.send_keys('Great juggling skills!')
        submit_button = self.browser.find_element_by_tag_name('button')
        submit_button.click()
        # The comment appears on the page
        self.wait_for(lambda: self.check_for_comment_in_comments_section('Great juggling skills!'))
        # There is no sign of the 'First post!' comment from the other video's page
        comments = self.browser.find_elements_by_class_name('comment')
        self.assertNotIn('First post!', [comment.text for comment in comments])
        self.assertEqual(len(comments), 1)

        # Feeling that they have missed an opportunity, the visitor adds another comment
        comment_field = self.browser.find_element_by_tag_name('textarea')
        comment_field.send_keys('Second post!')
        submit_button = self.browser.find_element_by_tag_name('button')
        submit_button.click()
        # Both comments are now visible on the page
        self.wait_for(lambda: self.check_for_comment_in_comments_section('Second post!'))
        self.check_for_comment_in_comments_section('Great juggling skills!')
