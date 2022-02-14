from django.test import TestCase
from django.urls import reverse
from vlog.models import JugglingVideo


class JugglingVideoSiteTest(TestCase):

    def check_context_dict_contains_correct_selected_item_for_view(self, view_name, desired_selected_value, arguments = None):
        """
        The context dict for a given view should contain the correct value for 'selected' in the context dict
        The selected class should appear on the appropriate page
        """
        # Note the name of this method cannot include test, because it is not intended to be run 'as is'
        # Create a test method in a sub-class and call this method from that test
        response = self.client.get(reverse(view_name, args = arguments))
        selected = response.context['selected']

        self.assertEqual(selected, desired_selected_value)
        self.assertContains(response, '<li class="navlink selected">')

    def post_video(self, video = 'first', pub_date = None):
        """
        Create a JugglingVideo objects from one of three videos
        A pub date can optionally be added via the relevant argument
        """

        videos = {
            'first': {
                'filename': 'five_ball_juggle_50_catches.mp4',
                'title': 'Five ball juggle 50 catches',
                'author_comment': 'This is the video that started it all!',
            },
            'second': {
                'filename': 'behind_the_back_juggle.mp4',
                'title': 'Behind the back juggle',
            },
            'third': {
                'filename': 'under_the_arm.mp4',
                'title': 'Under the arm juggle',
            },
        }

        kwargs = videos[video]

        if pub_date:
            kwargs['pub_date'] = pub_date

        return JugglingVideo.objects.create(**kwargs)

    def post_comment(self, video, text = '', author = ''):
        """
        Returns the response from POSTing a comment to the detail page for the video
        """
        data = {'text': text, 'author': author}

        return self.client.post(reverse('vlog:detail', args = [video.id]), data)

