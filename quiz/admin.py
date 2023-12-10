from django.contrib import admin

from .models import Country, Fact


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso2', 'continent')


class FactAdmin(admin.ModelAdmin):
    list_display = ('get_str', 'get_countries_names', 'category', 'question_type')
    list_filter = ('category', 'question_type', 'countries')

    def get_str(self, obj):
        return obj.__str__()
    get_str.short_description = 'Answer'

    def get_countries_names(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])


admin.site.register(Fact, FactAdmin)
admin.site.register(Country, CountryAdmin)
