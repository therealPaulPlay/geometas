from django.contrib import sitemaps
from django.urls import reverse

from quiz.models import Country, Category, Region

###########################################################
# Static pages
###########################################################

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
                'metas_index',
               ]

    def location(self, item):
        return reverse(item)
    

###########################################################
# Metas
###########################################################

class CountryMetasSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Country.objects.all().values_list('slug', flat=True)

    def location(self, item):
        return reverse('cms:country', args=[item])
    

class RegionMetasSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Region.objects.all().values_list('slug', flat=True)

    def location(self, item):
        return reverse('cms:region', args=[item])
    

class CategoryMetasSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Category.objects.all().values_list('slug', flat=True)

    def location(self, item):
        return reverse('cms:category', args=[item])