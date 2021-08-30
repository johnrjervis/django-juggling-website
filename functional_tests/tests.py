#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import tkinter as tk
import datetime as dt

class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.make_superuser()
        root = tk.Tk()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        # it seems that mint's menu bar is 64 pixels high
        self.gap = 2
        self.browser_height = int(screenheight - 64)
        self.browser_width = int((screenwidth / 2) - self.gap)
        root.destroy()

    def tearDown(self):
        self.browser.quit()

    def quit_if_possible(self, browser):
        try:
            browser.quit()
        except:
            pass

    def make_superuser(self):
        User.objects.create_superuser(username='admin_user', email='admin@jjs_juggling_site.com', password='secret_password')

    def datestring_to_datetime(self, datestring):
        """Converts the pub date (as it appears on the page) into a datetime object"""
        date, time = datestring.strip('Published on ').split(' at ')
        year, month, day = date.split('/')
        hours, minutes = time.split(':')
        datelist = [int(elem) for elem in [year, month, day, hours, minutes]]
        return dt.datetime(*datelist, tzinfo = dt.timezone.utc)

    def wait_for_element(self, element_type, search_method):
        start_time = time.time()
        while True:
            try:
                element = search_method(element_type)
            except WebDriverException as e:
                if time.time() > start_time + self.MAX_WAIT:
                    raise e
                time.sleep(0.5)
            else:
                time.sleep(1)
                return search_method(element_type)

    def test_full_site(self):

        # A net user stumbles across a cool juggling site
        visitor_browser = self.browser
        self.addCleanup(lambda: self.quit_if_possible(visitor_browser))
        self.browser.set_window_size(self.browser_width, self.browser_height)
        self.browser.set_window_position(0, 0)
        self.browser.get(f'{self.live_server_url}/juggling/')

        # On inspecting the site's title, the net user realises that this is none other than JJ's juggling site
        self.assertEqual("JJ's juggling site", self.browser.title)

        # The site's title element confirms it
        h1_elem = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("JJ's juggling videos", h1_elem)

        # However, the site has only just been launched, and no videos have been uploaded yet
        error_message = self.browser.find_element_by_id('id_error_message').text
        self.assertEqual('No videos are available!', error_message)
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 0)
        # There are also no links for further information on any videos
        further_info_links = self.wait_for_element('info_link', self.browser.find_elements_by_class_name)
        self.assertEqual(len(further_info_links), 0)

        # JJ logs in to the admin site and uploads the first video
        jj_browser = webdriver.Firefox()
        self.addCleanup(lambda: self.quit_if_possible(jj_browser))
        self.browser = jj_browser
        self.browser.set_window_size(self.browser_width, self.browser_height)
        time.sleep(1)
        self.browser.set_window_position(self.browser_width + (self.gap * 2), 0)
        self.browser.get(f'{self.live_server_url}/admin/')
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('admin_user')
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys('secret_password')
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)
        application_div = self.wait_for_element('app-vlog', self.browser.find_element_by_class_name)
        self.assertIn('Juggling videos', application_div.text)
        add_link = application_div.find_element_by_link_text('Add')
        add_link.click()
        time.sleep(1)
        new_video_field = self.wait_for_element('id_filename', self.browser.find_element_by_id)
        first_pub_date = timezone.now()
        first_video_filename = 'five_ball_juggle_50_catches.mp4'
        new_video_field.send_keys(first_video_filename)
        title_field = self.browser.find_element_by_id('id_title')
        first_title = 'Five ball juggle 50 catches'
        title_field.send_keys(first_title)
        #time.sleep(1)
        new_video_field.send_keys(Keys.ENTER)
        #time.sleep(4)

        # On returning to the page after the update, the net user sees a new video on the site
        self.browser = visitor_browser
        self.browser.refresh()
        time.sleep(1)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertIn(first_video_filename, videos[0].get_attribute('innerHTML'))
        # The user notices that there is a link for more information about the video
        further_info_link = self.wait_for_element('Click here for more information on this video', self.browser.find_element_by_link_text)
        self.assertIn('Click here for more information on this video', further_info_link.text)
        # The user clicks the link
        further_info_link.click()
        time.sleep(1)
        # The title of the video is displayed
        video_title = self.wait_for_element('detail_heading', self.browser.find_element_by_class_name)
        self.assertEqual(video_title.text, first_title)
        # The video's publication date is also displayed
        displayed_date_field = self.browser.find_element_by_class_name('video_pub_date')
        displayed_pub_date = self.datestring_to_datetime(displayed_date_field.text)
        #self.assertIn(first_pub_date, displayed_date.text) # Replaced by assertAlmostEqual statement below
        self.assertAlmostEqual(first_pub_date, displayed_pub_date, delta = dt.timedelta(minutes = 1))
        # The format of the further info link is the base url + videos/ + a number with at least one digit
        self.assertRegex(self.browser.current_url, r'/videos/\d+')
        # The user returns to the homepage
        homepage_link = self.browser.find_element_by_link_text('Home')
        homepage_link.click()
        #time.sleep(4)

        # Later on, JJ uploads another juggling video
        self.browser = jj_browser
        new_add_link = self.wait_for_element('ADD JUGGLING VIDEO', self.browser.find_element_by_link_text)
        new_add_link.click()
        new_video_field = self.wait_for_element('id_filename', self.browser.find_element_by_id)
        second_pub_date = timezone.now()
        self.assertGreaterEqual(second_pub_date, first_pub_date)
        second_video_filename = 'behind_the_back_juggle.mp4'
        new_video_field.send_keys(second_video_filename)
        title_field = self.browser.find_element_by_id('id_title')
        second_title = 'Behind the back juggle'
        title_field.send_keys(second_title)
        new_video_field.send_keys(Keys.ENTER)

        # The net user returns to the juggling site hoping to watch the first video again
        time.sleep(1)
        self.browser = visitor_browser
        self.browser.refresh() #get(f'{self.live_server_url}/juggling/')
        # However, the homepage now shows the newer video
        time.sleep(1)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertIn(second_video_filename, videos[0].get_attribute('innerHTML'))
        # The user clicks the archive link to see the original video
        archive_link = self.wait_for_element('Videos', self.browser.find_element_by_link_text)
        archive_link.click()
        # The original video is indeed in the archive
        video_title = self.wait_for_element('video_heading', self.browser.find_element_by_class_name)
        self.assertEqual(video_title.text, first_title)
        #time.sleep(24)
