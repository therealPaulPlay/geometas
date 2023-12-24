from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as django_sitemap_view
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
    path('admin/', admin.site.urls),
    path('quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('metas/', include(('cms.urls', 'cms'), namespace='cms')),
    path('learn/', include(('articles.urls', 'articles'), namespace='articles')),
    path('login/', accounts_login, name='login'),
    path('logout/', accounts_logout, name='logout'),
    path('sitemap.xml', django_sitemap_view, {'sitemaps': SITEMAPS_DICT}, name='django.contrib.sitemaps.views.sitemap'),
    #path('__debug__/', include('debug_toolbar.urls')),
    path('', metas_index, name='metas_index')
]
