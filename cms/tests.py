from django.test import TestCase

from cms.views import get_streetview_latlng

# Create test
class GetStreetviewLatlngTestCase(TestCase):
    def test_get_streetview_latlng(self):
        # Case 1
        url = 'https://consent.google.com/ml?continue=https://www.google.com/maps/@?api%3D1%26map_action%3Dpano%26pano%3Di9PWydJSef1m6Xc9cZXqhw%26viewpoint%3D41.973666,21.492935&gl=DE&m=0&pc=m&uxe=eomtm&cm=2&hl=de&src=1#extra%5BloadMode%5D=latLng'
        latlng = get_streetview_latlng(url)
        self.assertEqual(latlng, "41.973666,21.492935")
        
        # Case 2
        url = 'https://maps.app.goo.gl/Eymrxcn4ti3HYb7N7'
        latlng = get_streetview_latlng(url)
        self.assertEqual(latlng, "51.8705662,20.8451909")

