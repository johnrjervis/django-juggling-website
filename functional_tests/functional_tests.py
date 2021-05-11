from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_homepage_contents(self):

        # A netizen stumbles across a cool juggling site
        self.browser.get('http://localhost:8000')

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
        self.fail('Set up the admin site')

        # On returning to the page after the update the netizen sees a new video on the site
        # ...

if __name__ == '__main__':
    unittest.main(warnings='ignore')
