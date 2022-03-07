from django.test import TestCase
from django.urls import reverse
from vlog.tests.base import JugglingVideoSiteTest

# Create your tests here.

class ProgrammingViewTest(JugglingVideoSiteTest):
    """
    Tests for the programming page
    """

    def test_programming_page_uses_the_correct_template(self):
        """
        Check that the programming page uses the correct template
        """
        response = self.client.get(reverse('dev:programming'))

        self.assertTemplateUsed(response, 'dev/programming.html')

    def test_context_dict_contains_correct_selected_item_for_index_view(self):
        """
        The context dict for the home page view should contain 'selected': 'Programming'
        The selected class should be present on the programming page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('dev:programming', 'Programming')
