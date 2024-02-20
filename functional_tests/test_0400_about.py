from os import environ as os_environ
from .base import AdminAndSiteVisitorTest
from django.core import mail
from selenium.webdriver.common.action_chains import ActionChains

class T04AboutPagesTest(AdminAndSiteVisitorTest):
    """
    Tests for the about pages
    (Includes the History and Thanks pages)
    """
    def submit_form(self, form_dict):
        """Fills out a form using the supplied dictionary and then clicks the submit button"""
        for key in form_dict.keys():
            field = self.wait_for(lambda: self.browser.find_element_by_id(key))
            field.send_keys(form_dict[key])
        self.browser.find_element_by_tag_name('button').click()

    def test_about_pages(self):

        # JJ has added some acknowledgements via the admin site
        first_acknowledgement_details = {
            'name': 'Obey the Testing Goat!',
            'link': 'https://www.obeythetestinggoat.com/',
            'description': "I started out creating my juggling site by following the examples in Harry Percival's excellent book \"Test-Driven Development with Python\". I'd recommend buying a print copy if you're interested in web development with Python.",
        }
        self.create_database_object('Acknowledgement', first_acknowledgement_details)

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
        self.wait_for(lambda: self.assertEqual(flyout.is_displayed(), False))
        # But the flyout is displayed when the user hovers over the 'About' tab
        hover2 = ActionChains(self.browser).move_to_element(info_link)
        hover2.perform()
        #self.wait_for(lambda: self.assertEqual(flyout.value_of_css_property('visibility'), 'visible'))
        self.wait_for(lambda: self.assertEqual(flyout.is_displayed(), True))

    def test_contact_page(self):

        # A visitor accesses the contact page
        self.browser.get(f'{self.live_server_url}/juggling/about/contact/')
        # The visitor accidentally clicks the submit button without filling in the contact form
        self.submit_form({'message': ''})
        # A message appears to say that the message box must be filled in
        self.wait_for(lambda: self.assertIn("Please enter a message.", self.browser.find_element_by_tag_name('body').text))
        # JJ does not receive an email
        with self.assertRaises(AttributeError):
            mail.inbox[0] # it seems mail has no inbox attribute until an email is sent, hence this should raise an AttributeError
        # The visitor fills out the contact form and submits it
        visitor_message = {
            'message': 'I really like your website',
            'sender_name': 'A site visitor'
        }
        self.submit_form(visitor_message)
        # A message appears to say that the message has been sent
        self.wait_for(lambda: self.assertIn("Your message has been sent!", self.browser.find_element_by_tag_name('body').text))

        # JJ receives an email
        email = mail.outbox[0]
        self.assertIn(os_environ.get('EMAIL_ADDRESS'), email.to)
        self.assertIn(visitor_message['message'], email.body)
        self.assertIn(visitor_message['sender_name'], email.body)
