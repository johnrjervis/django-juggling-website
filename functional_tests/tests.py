from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import tkinter as tk
import datetime as dt

## Tests are run in alphabetical order of class, hence T01, T02, etc.

class JugglingWebsiteTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_element(self, element_identifier, search_method):
        start_time = time.time()
        while True:
            try:
                element = search_method(element_identifier)
            except WebDriverException as e:
                if time.time() > start_time + self.MAX_WAIT:
                    raise e
                time.sleep(0.5)
            else:
                time.sleep(1)
                return search_method(element_identifier)

class AdminAndSiteUserTest(JugglingWebsiteTest):

    def setUp(self):
        self.visitor_browser = webdriver.Firefox()
        self.jj_browser = webdriver.Firefox()

        root = tk.Tk()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        ## it seems that mint's menu bar is 64 pixels high
        gap = 0
        browser_height = int(screenheight - 64)
        browser_width = int((screenwidth / 2) - gap)
        root.destroy()

        User.objects.create_superuser(username='admin_user', email='admin@jjs_juggling_site.com', password='secret_password')

        self.visitor_browser.set_window_size(browser_width, browser_height)
        self.jj_browser.set_window_size(browser_width, browser_height)
        self.visitor_browser.set_window_position(0, 0)
        self.jj_browser.set_window_position(browser_width + (gap * 2), 0)

    def tearDown(self):
        self.jj_browser.quit()
        self.visitor_browser.quit()


class T01HomePageAndAdminSiteTest(AdminAndSiteUserTest):

    def test_homepage_and_admin_site(self):

        # A net user stumbles across a cool juggling site
        self.visitor_browser.get(self.live_server_url)

        # On inspecting the site's title, the net user realises that this is none other than JJ's juggling site
        self.assertEqual("JJ's juggling site", self.visitor_browser.title)

        # The site's title element confirms it
        h1_text = self.visitor_browser.find_element_by_tag_name('h1').text
        self.assertEqual("JJ's juggling videos", h1_text)

        # The site has a distinctive green colour scheme
        ## This section tests that the CSS has been applied
        site_header = self.visitor_browser.find_element_by_tag_name('header')
        site_header_colour = site_header.value_of_css_property('background-color')
        self.assertEqual(site_header_colour, 'rgb(100, 246, 100)')
        # And the home tab stands out in the navigation menu (because it has the 'selected' class applied)
        index_tab = self.visitor_browser.find_element_by_class_name('selected')
        self.assertEqual(index_tab.text, 'Home')

        # However, the site has only just been launched, and no videos have been uploaded yet
        error_message = self.visitor_browser.find_element_by_id('id_error_message').text
        self.assertEqual('No videos are available!', error_message)
        videos = self.visitor_browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 0)
        # There are also no links for further information on any videos
        further_info_links = self.wait_for_element('info_link', self.visitor_browser.find_elements_by_class_name)
        self.assertEqual(len(further_info_links), 0)

        # JJ logs in to the admin site and uploads the first video
        self.jj_browser.get(f'{self.live_server_url}/admin/')
        username_field = self.jj_browser.find_element_by_id('id_username')
        username_field.send_keys('admin_user')
        password_field = self.jj_browser.find_element_by_id('id_password')
        password_field.send_keys('secret_password')
        password_field.send_keys(Keys.ENTER)
        application_div = self.wait_for_element('app-vlog', self.jj_browser.find_element_by_class_name)
        self.assertIn('Juggling videos', application_div.text)
        add_link = application_div.find_element_by_link_text('Add')
        add_link.click()
        new_video_field = self.wait_for_element('id_filename', self.jj_browser.find_element_by_id)
        first_pub_date = timezone.now()
        first_video_filename = 'five_ball_juggle_50_catches.mp4'
        new_video_field.send_keys(first_video_filename)
        title_field = self.jj_browser.find_element_by_id('id_title')
        first_video_title = 'Five ball juggle 50 catches'
        title_field.send_keys(first_video_title)
        title_field.send_keys(Keys.ENTER)

        # On returning to the page after the update, the net user sees a new video on the site
        self.visitor_browser.refresh()
        time.sleep(1)
        videos = self.wait_for_element('video', self.visitor_browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertIn(first_video_filename, videos[0].get_attribute('innerHTML'))

        # Later on, JJ uploads another juggling video
        add_new_video_link = self.wait_for_element('ADD JUGGLING VIDEO', self.jj_browser.find_element_by_link_text)
        add_new_video_link.click()
        new_video_field = self.wait_for_element('id_filename', self.jj_browser.find_element_by_id)
        second_pub_date = timezone.now()
        self.assertGreaterEqual(second_pub_date, first_pub_date)
        second_video_filename = 'behind_the_back_juggle.mp4'
        new_video_field.send_keys(second_video_filename)
        title_field = self.jj_browser.find_element_by_id('id_title')
        second_video_title = 'Behind the back juggle'
        title_field.send_keys(second_video_title)
        title_field.send_keys(Keys.ENTER)

        # The site visitor returns to the juggling site to see the latest video
        time.sleep(1)
        self.visitor_browser.refresh()
        # The original video is no longer on the homepage
        time.sleep(1)
        videos = self.wait_for_element('video', self.visitor_browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertNotIn(first_video_filename, videos[0].get_attribute('innerHTML'))
        # The newer video appears in its place
        self.assertIn(second_video_filename, videos[0].get_attribute('innerHTML'))


class T02VideoArchiveAndDetailViewTest(AdminAndSiteUserTest):

    def check_for_comment_in_comments_table(self, comment_text):
        comment_table = self.wait_for_element('user_comments', self.visitor_browser.find_element_by_class_name)
        comment_rows = comment_table.find_elements_by_tag_name('tr')

        self.assertIn(comment_text, [comment_row.text for comment_row in comment_rows])

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
        application_div = self.wait_for_element('app-vlog', self.jj_browser.find_element_by_class_name)
        self.assertIn('Juggling videos', application_div.text)
        add_video_link = application_div.find_element_by_link_text('Add')
        add_video_link.click()
        new_video_field = self.wait_for_element('id_filename', self.jj_browser.find_element_by_id)
        ## Need to find a way to send times to the date field in the admin site if I want to adjust pub dates
        first_pub_date = timezone.now()
        first_video_filename = 'five_ball_juggle_50_catches.mp4'
        new_video_field.send_keys(first_video_filename)
        title_field = self.jj_browser.find_element_by_id('id_title')
        first_video_title = 'Five ball juggle 50 catches'
        title_field.send_keys(first_video_title)
        title_field.send_keys(Keys.ENTER)
        add_new_video_link = self.wait_for_element('ADD JUGGLING VIDEO', self.jj_browser.find_element_by_link_text)
        add_new_video_link.click()
        new_video_field = self.wait_for_element('id_filename', self.jj_browser.find_element_by_id)
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
        self.visitor_browser.get(f'{self.live_server_url}/juggling/')

        # The visitor notices that there is a link for more information about the video
        video_comment_link = self.wait_for_element('comment_link', self.visitor_browser.find_element_by_class_name)
        self.assertIn('Comment on this video', video_comment_link.text)
        # The user clicks the link
        video_comment_link.click()
        # The title of the video is displayed
        video_title = self.wait_for_element('detail_heading', self.visitor_browser.find_element_by_class_name)
        self.assertEqual(video_title.text, second_video_title)
        # The video's publication date is also displayed
        displayed_date_field = self.visitor_browser.find_element_by_class_name('video_pub_date')
        displayed_pub_date = self.datestring_to_datetime(displayed_date_field.text)
        #self.assertIn(first_pub_date, displayed_date.text) # Replaced by assertAlmostEqual statement below
        self.assertAlmostEqual(second_pub_date, displayed_pub_date, delta = dt.timedelta(seconds = 65))
        # The format of the further info link is the base url + videos/ + a number with at least one digit
        self.assertRegex(self.visitor_browser.current_url, r'/videos/\d+')

        # The visitor also sees an input field for posting comments
        comment_field = self.visitor_browser.find_element_by_tag_name('input')
        self.assertEqual(comment_field.get_attribute('placeholder'), 'Enter a comment')
        # The visitor enters a comment
        comment_field.send_keys('First post!')
        comment_field.send_keys(Keys.ENTER)
        # The comment appears on the page
        self.check_for_comment_in_comments_table('First post!')

        # Intrigued to see what other videos are available, the visitor clicks the archive link
        video_archive_link = self.visitor_browser.find_element_by_link_text('Videos')
        video_archive_link.click()
        # The latest video is not in the archive, but there is another video (which was posted about a week ago)
        videos = self.wait_for_element('video', self.visitor_browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertNotIn(second_video_filename, videos[0].get_attribute('innerHTML'))
        self.assertIn(first_video_filename, videos[0].get_attribute('innerHTML'))

        # Once again, there is a link for further information
        archive_video_comment_link = self.wait_for_element('comment_link', self.visitor_browser.find_element_by_class_name)
        # The user clicks the link
        archive_video_comment_link.click()
        # The title of this video is displayed
        video_title = self.wait_for_element('detail_heading', self.visitor_browser.find_element_by_class_name)
        self.assertEqual(video_title.text, first_video_title)
        # The video's publication date is also displayed - it is about a week old
        older_displayed_date_field = self.visitor_browser.find_element_by_class_name('video_pub_date')
        older_displayed_pub_date = self.datestring_to_datetime(older_displayed_date_field.text)
        self.assertAlmostEqual(first_pub_date, older_displayed_pub_date, delta = dt.timedelta(seconds = 65))

        # The visitor is surprised to see that no-one has commented on this video yet
        comments = self.wait_for_element('comment', self.visitor_browser.find_elements_by_class_name)
        self.assertNotIn('First post!', [comment.text for comment in comments])
        self.assertEqual(len(comments), 0)

        # The user enters another comment
        comment_field = self.visitor_browser.find_element_by_tag_name('input')
        comment_field.send_keys('Great juggling skills!')
        comment_field.send_keys(Keys.ENTER)
        time.sleep(1)
        # Feeling that they have missed an opportunity, the visitor adds another comment
        comment_field = self.visitor_browser.find_element_by_tag_name('input')
        comment_field.send_keys('Second post!')
        comment_field.send_keys(Keys.ENTER)
        # Both comments are now visible on the page
        self.check_for_comment_in_comments_table('Great juggling skills!')
        self.check_for_comment_in_comments_table('Second post!')


class T03LearnPageTest(JugglingWebsiteTest):

    def test_learn_page(self):

        # A site visitor decides to visit the learn page
        self.browser.get(f'{self.live_server_url}/juggling/learn/')

        # However, the user finds that this part of the site has not been completed yet
        para = self.wait_for_element('p', self.browser.find_element_by_tag_name)
        self.assertEqual(para.text, 'This part of the site is still under construction.')


class T04AboutPagesTest(JugglingWebsiteTest):

    def test_about_pages(self):

        # Another visitor accesses the website
        self.browser.get(f'{self.live_server_url}/juggling/')
        # The visitor clicks on the info link to find out more about the juggling site
        info_link = self.wait_for_element('About', self.browser.find_element_by_link_text)
        info_link.click()

        para = self.wait_for_element('p', self.browser.find_element_by_tag_name)
        self.assertEqual(para.text, 'Did I mention that this is my website for showing off my juggling skills?')

        # This page contains liks to information pages
        about_page_main_section = self.browser.find_element_by_tag_name('main')
        page_links = about_page_main_section.find_elements_by_tag_name('a')
        self.assertGreater(len(page_links), 0)
        # The visitor clicks on a link to the thanks page where JJ acknowledges some useful resources
        thanks_link = self.browser.find_element_by_link_text('Thanks')
        thanks_link.click()
        # There is a mention for the testing goat!
        thanks_page_main = self.wait_for_element('main', self.browser.find_element_by_tag_name)
        self.assertIn('Testing Goat', thanks_page_main.text)
        # The user goes back to the about page
        self.browser.back()
        # There is also a link to the history of the site on the About page
        history_link = self.wait_for_element('History', self.browser.find_element_by_link_text)
        history_link.click()
        history_page_main = self.wait_for_element('main', self.browser.find_element_by_tag_name)
        self.assertIn('a series of juggling videos', history_page_main.text)

        # The user realises that the history and thanks pages can also be accessed from a flyout menu on the about tab
        info_link = self.browser.find_element_by_link_text('About')
        flyout = self.browser.find_element_by_class_name('flyout')
        # The flyout menu is hidden by default
        self.assertEqual(flyout.value_of_css_property('visibility'), 'hidden')
        # But the flyout is displayed when the user hovers over the 'About' tab
        hover = ActionChains(self.browser).move_to_element(info_link)
        hover.perform()
        self.assertEqual(flyout.value_of_css_property('visibility'), 'visible')

