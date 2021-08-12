#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        # JJ logs in to the admin site and uploads a new video
        jj_browser = webdriver.Firefox()
        self.addCleanup(lambda: self.quit_if_possible(jj_browser))
        self.browser = jj_browser
        self.browser.get(f'{self.live_server_url}/admin/')
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
        fv_pub_date = timezone.now().strftime(format = '%Y/%m/%d at %H:%M')
        first_video_filename = 'five_ball_juggle_50_catches.mp4'
        new_video_field.send_keys(first_video_filename)
        title_field = self.browser.find_element_by_id('id_title')
        fv_title = 'Five ball juggle 50 catches'
        title_field.send_keys(fv_title)
        #time.sleep(1)
        new_video_field.send_keys(Keys.ENTER)
        #time.sleep(4)

        # On returning to the page after the update, the net user sees a new video on the site
        self.browser = visitor_browser
        self.browser.refresh()
        #time.sleep(4)
        videos = self.wait_for_element('video', self.browser.find_elements_by_tag_name)
        self.assertEqual(len(videos), 1)
        self.assertIn(first_video_filename, videos[0].get_attribute('innerHTML'))
        # The user notices that there is a link for more information about the video
        further_info_link = self.wait_for_element('info_link', self.browser.find_element_by_class_name)
        self.assertIn('Click here for more information on this video', further_info_link.text)
        #time.sleep(4)
        # The user clicks the link
        further_info_link.click()
        # The title of the video is displayed
        video_title = self.wait_for_element('detail_heading', self.browser.find_element_by_class_name)
        self.assertEqual(video_title.text, fv_title)
        # The video's publication date is also displayed
        displayed_date = self.browser.find_element_by_class_name('video_pub_date')
        self.assertIn(fv_pub_date, displayed_date.text)
        # The format of the further info link is the base url + videos/ + a number with at least one digit
        self.assertRegex(self.browser.current_url, r'/videos/\d+')
        #time.sleep(4)

