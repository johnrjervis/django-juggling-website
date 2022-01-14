from .base import AdminAndSiteVisitorTest
from django.utils import timezone
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime as dt


class T01HomePageAndAdminSiteTest(AdminAndSiteVisitorTest):

    def test_homepage_and_admin_site(self):

        # A net user stumbles across a cool juggling site
        self.browser.get(self.live_server_url)

        # On inspecting the site's title, the net user realises that this is none other than JJ's juggling site
        self.assertEqual("JJ's juggling site", self.browser.title)

        # The site's title element confirms it
        h1_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("JJ's juggling videos", h1_text)

        # The site has a distinctive green colour scheme
        ## This section tests that the CSS has been applied
        site_header = self.browser.find_element_by_tag_name('header')
        site_header_colour = site_header.value_of_css_property('background-color')
        self.assertEqual(site_header_colour, 'rgb(100, 246, 100)')
        # And the home tab stands out in the navigation menu (because it has the 'selected' class applied)
        index_tab = self.browser.find_element_by_class_name('selected')
        self.assertEqual(index_tab.text, 'Home')

        # However, the site has only just been launched, and no videos have been uploaded yet
        error_message = self.browser.find_element_by_id('id_error_message').text
        self.assertEqual('No videos are available!', error_message)
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 0)
        # There are also no links for further information on any videos
        further_info_links = self.wait_for_element('info_link', self.browser.find_elements_by_class_name)
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
        self.browser.refresh()
        time.sleep(1)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
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
        self.browser.refresh()
        # The original video is no longer on the homepage
        time.sleep(1)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertNotIn(first_video_filename, videos[0].get_attribute('innerHTML'))
        # The newer video appears in its place
        self.assertIn(second_video_filename, videos[0].get_attribute('innerHTML'))

