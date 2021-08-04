#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.common.exceptions import WebDriverException
import time

class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.make_superuser()

    def tearDown(self):
        self.browser.quit()

    def quit_if_possible(self, browser):
        try:
            browser.quit()
        except:
            pass

    def make_superuser(self):
        User.objects.create_superuser(username='admin_user', email='admin@jjs_juggling_site.com', password='secret_password')

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
                return element

    def test_homepage_contents(self):

        # A net user stumbles across a cool juggling site
        visitor_browser = self.browser
        self.addCleanup(lambda: self.quit_if_possible(visitor_browser))
        self.browser.get(self.live_server_url)

        # On inspecting the site's title, netizen realises that this is none other than JJ's juggling site
        self.assertEqual("JJ's juggling site", self.browser.title)

        # The site's title element confirms it
        h1_elem = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("JJ's juggling videos", h1_elem)

        # However, the site has only just been launched, and no videos have been uploaded yet
        error_message = self.browser.find_element_by_id('id_error_message').text
        self.assertEqual('No videos are available!', error_message)
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 0)

        # JJ logs in to the admin site and uploads a new video
        jj_browser = webdriver.Firefox()
        self.addCleanup(lambda: self.quit_if_possible(jj_browser))
        self.browser = jj_browser
        self.browser.get(f'{self.live_server_url}/admin')
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('admin_user')
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys('secret_password')
        password_field.send_keys(Keys.ENTER)
        #time.sleep(4)
        application_div = self.wait_for_element('model-jugglingvideo', self.browser.find_element_by_class_name)
        self.assertIn('Juggling videos', application_div.text)
        add_link = application_div.find_element_by_class_name('addlink')
        add_link.click()
        #time.sleep(4)
        new_video_field = self.wait_for_element('id_filename', self.browser.find_element_by_id)
        new_video_field.send_keys('five_ball_juggle_50_catches.mp4')
        #time.sleep(1)
        new_video_field.send_keys(Keys.ENTER)
        #time.sleep(4)

        # On returning to the page after the update the net user sees a new video on the site
        self.browser = visitor_browser
        self.browser.refresh()
        #time.sleep(4)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertIn('five_ball_juggle_50_catches.mp4', videos[0].get_attribute('innerHTML'))

