from .base import JugglingWebsiteTest


class T03LearnPageTest(JugglingWebsiteTest):
    """
    Tests for the learn page
    """

    def test_learn_page(self):

        # A site visitor decides to visit the learn page
        self.browser.get(f'{self.live_server_url}/juggling/learn/')

        # However, the user finds that this part of the site has not been completed yet
        self.wait_for(lambda: self.assertIn('still under construction', self.browser.find_element_by_tag_name('p').text))

