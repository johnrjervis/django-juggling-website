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

        # There is information about JJ's programming experience
        self.wait_for(
            lambda: self.find_substring_in_elements('Python', 'li')
        )
