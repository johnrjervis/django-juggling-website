from .base import AdminAndSiteVisitorTest
from selenium.webdriver.common.action_chains import ActionChains

class T04AboutPagesTest(AdminAndSiteVisitorTest):
    """
    Tests for the about pages
    (Includes the History and Thanks pages)
    """

    def test_about_pages(self):

        # JJ has added some acknowledgements via the admin site
        acks_admin_link = self.wait_for(lambda: self.jj_browser.find_element_by_link_text('Acknowledgements'))
        acks_admin_link.click()
        add_ack_link = self.wait_for(lambda: self.jj_browser.find_element_by_link_text('ADD ACKNOWLEDGEMENT'))
        add_ack_link.click()
        ack_name_field = self.wait_for(lambda: self.jj_browser.find_element_by_id('id_name'))
        first_ack_name = 'Obey the Testing Goat!'
        ack_name_field.send_keys(first_ack_name)
        link_field = self.jj_browser.find_element_by_id('id_link')
        first_ack_link = 'https://www.obeythetestinggoat.com/'
        link_field.send_keys(first_ack_link)
        description_field = self.jj_browser.find_element_by_id('id_description')
        first_ack_description = "I started out creating my juggling site by following the examples in Harry Percival's excellent book \"Test-Driven Development with Python\". I'd recommend buying a print copy if you're interested in web development with Python."
        description_field.send_keys(first_ack_description)
        save_ack_update = self.jj_browser.find_element_by_name('_save')
        save_ack_update.click()

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
        home_link = self.browser.find_element_by_link_text('Home')
        info_link = self.browser.find_element_by_link_text('About')
        flyout = self.browser.find_element_by_class_name('flyout')
        # The flyout menu is hidden by default
        hover1 = ActionChains(self.browser).move_to_element(home_link)
        hover1.perform()
        self.wait_for(lambda: self.assertEqual(flyout.value_of_css_property('visibility'), 'hidden'))
        # But the flyout is displayed when the user hovers over the 'About' tab
        hover2 = ActionChains(self.browser).move_to_element(info_link)
        hover2.perform()
        self.wait_for(lambda: self.assertEqual(flyout.value_of_css_property('visibility'), 'visible'))

