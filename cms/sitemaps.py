from django.contrib import sitemaps
from django.urls import reverse

from quiz.models import Country, Fact, CATEGORY_CHOICES

###########################################################
# Static pages
###########################################################

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
                'home',
                'cms:metas_index',
                'quiz:quiz_index',
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
        return Country.objects.all().values_list('region_slug', flat=True).distinct()

    def location(self, item):
        return reverse('cms:region', args=[item])
    

class CategoryMetasSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [category[0] for category in CATEGORY_CHOICES]

    def location(self, item):
        return reverse('cms:category', args=[item])