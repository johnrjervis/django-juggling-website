from .base import AdminAndSiteVisitorTest
from django.utils import timezone
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class T01HomePageAndAdminSiteTest(AdminAndSiteVisitorTest):

    def test_homepage_and_admin_site(self):

        # A net user stumbles across a cool juggling site
        self.browser.get(self.live_server_url)

        # On inspecting the site's title, the net user realises that this is none other than JJ's juggling site
        self.wait_for(lambda: self.assertEqual("JJ's juggling site", self.browser.title))

        # The site's title element confirms it
        h1_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("JJ's Juggling Videos", h1_text)

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
        self.wait_for(lambda: self.assertEqual(len(self.browser.find_elements_by_class_name('info_link')), 0))

        # JJ logs in to the admin site and uploads the first video
        ## Setting the date to a couple of days ago ensures that its pub date will be older than the second video
        date_for_first_video = timezone.now() - timedelta(days = 2)
        first_video_pub_date, _ = self.format_datetime_obj_for_admin_page(date_for_first_video)
        first_video_details =   {
                                'filename': 'five_ball_juggle_50_catches.mp4',
                                'title': 'Five ball juggle 50 catches',
                                'pub_date_0': first_video_pub_date,
                                }
        self.create_database_object('Juggling video', first_video_details)

        # On returning to the page after the update, the net user sees a new video on the site
        self.browser.refresh()
        self.wait_for(lambda: self.assertEqual(len(self.browser.find_elements_by_tag_name('video')), 1))
        video = self.browser.find_element_by_tag_name('video')
        self.assertIn(first_video_details['filename'], video.get_attribute('innerHTML'))

        # Later on, JJ uploads another juggling video
        ## If no date info is submitted, then the pub date defaults to the current time
        second_video_details =   {
                                'filename': 'behind_the_back_juggle.mp4',
                                'title': 'Behind the back juggle',
                                }
        self.create_database_object('Juggling video', second_video_details)

        # The site visitor returns to the juggling site's home page to see the latest video
        self.browser.refresh()
        # The new video now appears on the home page
        self.wait_for(lambda: self.assertIn(second_video_details['filename'], self.browser.find_element_by_tag_name('video').get_attribute('innerHTML')))
        updated_videos = self.browser.find_elements_by_tag_name('video')
        # It is the only video on the page and there is no sign of the first video
        self.assertEqual(len(updated_videos), 1)
        self.assertNotIn(first_video_details['filename'], updated_videos[0].get_attribute('innerHTML'))

