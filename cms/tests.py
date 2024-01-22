from django.test import TestCase

from cms.views import parce_viewpoint_from_url


class GetStreetviewLatlngTestCase(TestCase):
    def test_get_streetview_latlng(self):
        url = 'https://consent.google.com/ml?continue=https://www.google.com/maps/@?api%3D1%26map_action%3Dpano%26pano%3Di9PWydJSef1m6Xc9cZXqhw%26viewpoint%3D41.973666,21.492935&gl=DE&m=0&pc=m&uxe=eomtm&cm=2&hl=de&src=1#extra%5BloadMode%5D=latLng'
        latlng = parce_viewpoint_from_url(url)
        self.assertEqual(latlng, "41.973666,21.492935")
        
        url = 'https://consent.google.com/ml?continue=https://www.google.com/maps/@48.2053212,16.3711711,3a,24.674866y,41.462292h,108.423958t/data%3D!3m4!1e1!3m2!1sL7JW6LpMrVpTy0_0br2Xrw!2e0?lucs%3D,47071704,47069508,47084304%26g_ep%3DCAISDDYuOTYuMS4zMDU4MBgAIIGBASobLDQ3MDcxNzA0LDQ3MDY5NTA4LDQ3MDg0MzA0QgJERQ%253D%253D%26g_st%3Dic&gl=DE&m=0&pc=m&uxe=eomtm&cm=2&hl=de&src=1'
        latlng = parce_viewpoint_from_url(url)
        self.assertEqual(latlng, "48.2053212,16.3711711")

        url = 'https://consent.google.com/ml?continue=https://www.google.com/maps/@11.2150006,-73.3319606,3a,26.5y,137.16h,77.86t,0.36r/data%3D!3m6!1e1!3m4!1s8H30yAU3MC20ziErailssQ!2e0!7i16384!8i8192?entry%3Dtts&gl=DE&m=0&pc=m&uxe=eomtm&cm=2&hl=de&src=1'
        latlng = parce_viewpoint_from_url(url)
        self.assertEqual(latlng, "11.2150006,-73.3319606")
