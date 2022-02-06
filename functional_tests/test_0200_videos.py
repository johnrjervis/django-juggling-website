from .base import AdminAndSiteVisitorTest
from django.utils import timezone
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class T02VideoArchiveAndDetailViewTest(AdminAndSiteVisitorTest):

    def check_for_text_in_css_class_list(self, text, css_class, not_in = False):
        """Finds a list of elements with a given CSS class and checks for the presence of the text in that list"""
        class_list = self.browser.find_elements_by_class_name(css_class)

        if not_in:
            self.assertNotIn(text, [element.text for element in class_list])
        else:
            self.assertIn(text, [element.text for element in class_list])

    def convert_datestring_to_datetime(self, datestring):
        """Converts the pub date (as it appears on the page) into a datetime object"""
        date, time = datestring.strip('Published on ').split(' at ')
        day, month, year = date.split('/')
        hours, minutes = time.split(':')
        datelist = [int(elem) for elem in [year, month, day, hours, minutes]]
        return datetime(*datelist, tzinfo = timezone.utc)

    def post_video_comment(self, text, comment_author = None):
        """Posts a comment via the form on a video detail page"""
        comment_field = self.browser.find_element_by_class_name('comments_box')
        comment_field.send_keys(text)
        if comment_author:
            name_field = self.browser.find_element_by_class_name('commenter_name')
            name_field.send_keys(comment_author)
        submit_button = self.browser.find_element_by_tag_name('button')
        submit_button.click()

    def format_datetime_obj_for_comparison_with_website(self, obj):
        """Converts a datetime object into the string format displayed on the site"""
        return f'Published on {obj.day:02}/{obj.month:02}/{obj.year} at {obj.hour:02}:{obj.minute:02}'

    def test_detail_views_and_video_archive(self):

        # JJ has already uploaded a couple of videos to the site
        # The first video was published about a week ago (time also changed to differentiate from 2nd pub time)
        date_for_first_video = timezone.now() - timedelta(days = 7, hours = 1, minutes = 14)
        first_video_pub_date, first_video_pub_time = self.format_datetime_obj_for_admin_page(date_for_first_video)
        first_video_details = {
            'filename': 'five_ball_juggle_50_catches.mp4',
            'title': 'Five ball juggle 50 catches',
            'pub_date_0': first_video_pub_date,
            'pub_date_1': first_video_pub_time,
            'author_comment': 'This was the video that started it all!',
        }
        self.create_database_object('Juggling video', first_video_details)

        # A second video was added at midnight today
        date_for_second_video = timezone.now()
        second_video_pub_date, second_video_pub_time = self.format_datetime_obj_for_admin_page(date_for_second_video)
        second_video_details = {
            'filename': 'behind_the_back_juggle.mp4',
            'title': 'Behind the back juggle',
            'pub_date_0': second_video_pub_date,
            'pub_date_1': second_video_pub_time,
            'author_comment': 'This video was recorded in hotel quarantine',
        }
        self.create_database_object('Juggling video', second_video_details)

        # A site visitor goes to the homepage
        self.browser.get(f'{self.live_server_url}/juggling/')

        # The visitor notices that there is a link for commenting on the video
        video_comment_link = self.wait_for(lambda: self.browser.find_element_by_class_name('comment_link'))
        self.assertIn('Comment on this video', video_comment_link.text)
        # The user clicks the link
        video_comment_link.click()
        # The title of the video is displayed
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_class_name('detail_heading').text, second_video_details['title']))
        # JJ's comments on the video are displayed
        self.check_for_text_in_css_class_list('This video was recorded in hotel quarantine', 'author_comment')
        # The video's publication date is also displayed
        displayed_home_date = self.browser.find_element_by_class_name('video_pub_date').text
        expected_home_date = self.format_datetime_obj_for_comparison_with_website(date_for_second_video)
        self.assertEqual(displayed_home_date, expected_home_date)
        # The format of the further info link is the base url + videos/ + a number with at least one digit
        self.assertRegex(self.browser.current_url, r'/videos/\d+')

        # The visitor sees an input field for posting comments
        comment_field = self.browser.find_element_by_class_name('comments_box')
        self.assertEqual(comment_field.get_attribute('placeholder'), 'Enter your comment')
        # There is also a field for entering a name to go with the comment
        name_field = self.browser.find_element_by_class_name('commenter_name')
        self.assertEqual(name_field.get_attribute('placeholder'), 'Enter your name (optional)')
        # No comments have been posted  on this video yet, and there is an invite to post the first comment
        self.check_for_text_in_css_class_list('There are no comments for this video yet. Use the form below to post the first comment!', 'comment_invite')
        # The visitor enters a comment and clicks the 'Post comment' button
        self.post_video_comment('First post!')
        submit_date = timezone.now()
        # The comment appears on the page
        self.wait_for(lambda: self.check_for_text_in_css_class_list('First post!', 'comment_text'))
        # Because the visitor did not enter a name, the comment is listed as being posted by anonymous
        self.check_for_text_in_css_class_list('Posted by anonymous', 'comment_author')
        # The time of the comment is also displayed
        displayed_comment_date = self.wait_for(lambda: self.browser.find_element_by_class_name('comment_date').text)
        comment_date = self.convert_datestring_to_datetime(displayed_comment_date)
        self.assertAlmostEqual(submit_date, comment_date, delta = timedelta(minutes = 2))
        # The invite to post the first comment has disappeared
        self.check_for_text_in_css_class_list('There are no comments for this video yet. Use the form below to post the first comment!',  'comment_invite', not_in = True)
        # The visitor decides to add another comment, this time they do add a name for the comment
        self.post_video_comment('Great juggling skills!', comment_author = 'Site visitor')
        self.wait_for(lambda: self.check_for_text_in_css_class_list('Great juggling skills!', 'comment_text'))
        self.check_for_text_in_css_class_list('Posted by Site visitor', 'comment_author')

        # Intrigued to see what other videos are available, the visitor clicks the archive link
        video_archive_link = self.browser.find_element_by_link_text('Videos')
        video_archive_link.click()
        # The first video posted to the site is in the archive
        self.wait_for(lambda: self.assertIn(first_video_details['filename'], self.browser.find_element_by_tag_name('video').get_attribute('innerHTML')))
        # This is the only video in the archive, as the video on the home page has not been moved to the archive yet 
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 1)
        self.assertNotIn(second_video_details['filename'], videos[0].get_attribute('innerHTML'))

        # Once again, there is a link for comments
        archive_video_comment_link = self.wait_for(lambda: self.browser.find_element_by_class_name('comment_link'))
        # The user clicks the link
        archive_video_comment_link.click()
        # The title of this video is displayed
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_class_name('detail_heading').text, first_video_details['title']))
        # The archive video's publication date is also displayed
        displayed_archive_date = self.browser.find_element_by_class_name('video_pub_date').text
        expected_archive_date = self.format_datetime_obj_for_comparison_with_website(date_for_first_video)
        self.assertEqual(displayed_archive_date, expected_archive_date)
        # Again, JJ's comments on the video are also displayed
        self.check_for_text_in_css_class_list('This was the video that started it all!', 'author_comment')

        # The user enters a comment for this video
        self.post_video_comment('Impressive!')
        self.wait_for(lambda: self.check_for_text_in_css_class_list('Impressive!', 'comment_text'))
        # There is no sign of the comments from the other video's page
        self.check_for_text_in_css_class_list('First post!', 'comment_text', not_in = True)
        self.check_for_text_in_css_class_list('Great juggling skills!', 'comment_text', not_in = True)
        comments = self.browser.find_elements_by_class_name('comment_text')
        self.assertEqual(len(comments), 1)

        # The user enters a silly comment
        self.post_video_comment('I can has a cheezburger?', comment_author = 'Lolzcat')

        # JJ removes this comment from the website
        comment_admin_link = self.jj_browser.find_element_by_link_text('Video comments')
        comment_admin_link.click()
        silly_comment_link = self.wait_for(lambda: self.jj_browser.find_element_by_link_text('Comment: I can has a cheezburger?'))
        silly_comment_link.click()
        enable_checkbox = self.wait_for(lambda: self.jj_browser.find_element_by_id('id_is_approved'))
        enable_checkbox.click()
        save_comment_update = self.jj_browser.find_element_by_name('_save')
        save_comment_update.click()

        # The comment no longer appears on the relevant video's detail page
        self.browser.refresh()
        self.wait_for(lambda: self.check_for_text_in_css_class_list('I can has a cheezburger?', 'comment_text', not_in = True))
        # The first comment is still there, however
        self.check_for_text_in_css_class_list('Impressive!', 'comment_text')

        # The visitor then accidentally clicks the submit button while the comment field is empty
        submit_button = self.browser.find_element_by_tag_name('button')
        submit_button.click()
        # The page refreshes and displays a warning to say that the blank comment could not be submitted
        self.wait_for(lambda: self.check_for_text_in_css_class_list('Blank comment was not submitted!', 'comment_warning'))


