from django.contrib import sitemaps
from django.urls import reverse

from quiz.models import Country, Category, Region, Fact

###########################################################
# Static pages
###########################################################

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
                'metas_index',
                'articles:country_coverage',
                'articles:driving_direction',
                'articles:eastern_europe',
                'articles:world_map_common_locations',
                'articles:south_african_countries',
                'articles:latin_america',
                'articles:nordics',
                'articles:australia_new_zealand',
                'articles:south_east_asia',
                'articles:baltics',
                'articles:central_africa',
               ]

    def location(self, item):
        return reverse(item)
    

###########################################################
# Index Pages
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


###########################################################
# Meta Details Pages
###########################################################

class MetasDetailSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Fact.objects.all().values_list('uuid', flat=True)

    def location(self, item):
        return reverse('cms:fact_detail', args=[item])
    
