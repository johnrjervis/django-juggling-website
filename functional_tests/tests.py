#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import time

class NewVisitorTest(StaticLiveServerTestCase):

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

        ### Need to log in to admin to set video #1.
        ### May have to use Seleniums send keys etc. (see ch.5 for this)
        ### Need to check video title, not just video element

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
        time.sleep(10)
        pagebody = self.browser.find_element_by_tag_name('body')
        self.assertIn('jugglingvideo', pagebody.text)
        #self.fail('Set up the admin site')

        # On returning to the page after the update the net user sees a new video on the site
        # ...

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
