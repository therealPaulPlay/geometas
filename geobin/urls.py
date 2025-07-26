from django.contrib.sitemaps.views import sitemap as django_sitemap_view
from django.views.generic.base import TemplateView
from django.urls import include, path

from cms.views import metas_index
import cms.sitemaps
from accounts.views import accounts_login, accounts_logout

SITEMAPS_DICT = {
    'static': cms.sitemaps.StaticViewSitemap,
    'country': cms.sitemaps.CountryMetasSitemap,
    'region': cms.sitemaps.RegionMetasSitemap,
    'category': cms.sitemaps.CategoryMetasSitemap,
    'metas': cms.sitemaps.MetasDetailSitemap
}


urlpatterns = [
    path('quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('metas/', include(('cms.urls', 'cms'), namespace='cms')),
    path('learn/', include(('articles.urls', 'articles'), namespace='articles')),
    path('api/metas/', include(('api.urls', 'api'), namespace='api')),
    path('login/', accounts_login, name='login'),
    path('logout/', accounts_logout, name='logout'),
    path('sitemap.xml', django_sitemap_view, {'sitemaps': SITEMAPS_DICT}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', metas_index, name='metas_index')
]
