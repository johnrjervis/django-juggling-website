from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class IndexViewTest(TestCase):
    """
    Tests for the programming page
    """

    def test_programming_page_uses_the_correct_template(self):
        """
        Check that the programming page uses the correct template
        """
        response = self.client.get(reverse('dev:programming'))

        self.assertTemplateUsed(response, 'dev/programming.html')
