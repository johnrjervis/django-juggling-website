from .base import JugglingWebsiteTest
from selenium.webdriver.common.action_chains import ActionChains


class T04AboutPagesTest(JugglingWebsiteTest):
    """
    Tests for the about pages
    (Includes the History and Thanks pages)
    """

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

