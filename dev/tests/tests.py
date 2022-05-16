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

    def test_context_dict_contains_correct_selected_item_for_programming_view(self):
        """
        The context dict for the programming view should contain 'selected': 'Programming'
        The selected class should be present on the programming page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('dev:programming', 'Programming')

class WebDevViewTest(JugglingVideoSiteTest):
    """
    Tests for the web development page
    """

    def test_web_development_page_uses_the_correct_template(self):
        """
        Check that the programming page uses the correct template
        """
        response = self.client.get(reverse('dev:web_development'))

        self.assertTemplateUsed(response, 'dev/web_development.html')

    def test_context_dict_contains_correct_selected_item_for_web_development_view(self):
        """
        The context dict for the web development view should contain 'selected': 'Web development'
        The selected class should be present on the web development page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('dev:web_development', 'Web development')

class PortfolioViewTest(JugglingVideoSiteTest):
    """
    Tests for the portfolio page
    """

    def test_portfolio_page_uses_the_correct_template(self):
        """
        Check that the portfolio page uses the correct template
        """
        response = self.client.get(reverse('dev:portfolio'))

        self.assertTemplateUsed(response, 'dev/portfolio.html')

    def test_context_dict_contains_correct_selected_item_for_portfolio_view(self):
        """
        The context dict for the portfolio view should contain 'selected': 'Portfolio'
        The selected class should be present on the web portfolio page
        """
        self.check_context_dict_contains_correct_selected_item_for_view('dev:portfolio', 'Portfolio')

