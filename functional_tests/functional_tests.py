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

        # There is a video on the home page
        videos = self.browser.find_elements_by_tag_name('video')
        self.assertEqual(len(videos), 1)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
