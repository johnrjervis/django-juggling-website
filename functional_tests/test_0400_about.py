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
        info_link = self.wait_for(lambda: self.browser.find_element_by_link_text('About'))
        info_link.click()
        # This page invites the visitor to find out more
        self.wait_for(lambda: self.assertIn('Find out more', self.browser.find_element_by_tag_name('main').text))
        # The further information is provided in links to pages in the main section of the page
        ## I've selected the main section so that the links in the navigation menu are ignored
        about_page_main_section = self.browser.find_element_by_tag_name('main')
        page_links = about_page_main_section.find_elements_by_tag_name('a')
        self.assertGreater(len(page_links), 0)

        # The visitor clicks on a link to the thanks page where JJ acknowledges some useful resources
        thanks_link = self.browser.find_element_by_link_text('Thanks')
        thanks_link.click()
        # There is a mention for the testing goat!
        self.wait_for(lambda: self.assertIn('Testing Goat', self.browser.find_element_by_tag_name('main').text))
        # The user goes back to the about page
        self.browser.back()
        # There is also a link to the history of the site on the About page
        history_link = self.wait_for(lambda: self.browser.find_element_by_link_text('History'))
        history_link.click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_tag_name('h2').text, 'The history of this site'))

        # The user realises that the history and thanks pages can also be accessed from a flyout menu on the about tab
        info_link = self.browser.find_element_by_link_text('About')
        flyout = self.browser.find_element_by_class_name('flyout')
        # The flyout menu is hidden by default
        self.assertEqual(flyout.value_of_css_property('visibility'), 'hidden')
        # But the flyout is displayed when the user hovers over the 'About' tab
        hover = ActionChains(self.browser).move_to_element(info_link)
        hover.perform()
        self.assertEqual(flyout.value_of_css_property('visibility'), 'visible')

