from .base import JugglingWebsiteTest

class T05DeveloperPageTest(JugglingWebsiteTest):
    """
    Tests for the developer pages
    """

    def find_substring_in_elements(self, text, tag):
        """
        Check whether the supplied text is a substring of any of the elements of the specified tag type
        """
        matched_elements = self.browser.find_elements_by_tag_name(tag)

        self.assertTrue(
            any(text in elem.text for elem in matched_elements),
            f'{text} was not found in the <{tag}> elements'
        )

    def test_programming_page(self):

        # A site visitor decides to visit the programming page
        self.browser.get(f'{self.live_server_url}/dev/programming/')

        # This part of the site has a different colour scheme to the main site
        ## This section tests that the CSS has been applied
        site_header = self.browser.find_element_by_tag_name('header')
        site_header_colour = site_header.value_of_css_property('background-color')
        self.assertEqual(site_header_colour, 'rgb(200, 200, 246)')

        # There is information about JJ's programming experience
        self.wait_for(
            lambda: self.find_substring_in_elements('Python', 'li')
        )

    def test_web_development_page(self):

        # A site visitor visits the web development page
        self.browser.get(f'{self.live_server_url}/dev/web-development/')

        # There is information about JJ's web development experience
        self.wait_for(
            lambda: self.find_substring_in_elements('Django', 'li')
        )
