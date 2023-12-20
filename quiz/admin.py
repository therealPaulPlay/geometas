from django.contrib import admin

from .models import Country, Fact, Quiz, QuizSession, QuizSessionFact, Category, Region


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso2', 'continent')


class FactAdmin(admin.ModelAdmin):
    list_display = ('get_str', 'get_countries_names', 'category')
    list_filter = ( 'countries', 'category') 

    def get_str(self, obj):
        return obj.__str__()
    get_str.short_description = 'Answer'

    def get_countries_names(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_countries_names', 'category')
    list_filter = ('countries', 'category') 

    def get_countries_names(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])
    get_countries_names.short_description = 'Countries'
    

class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'state', )
    readonly_fields = ('quiz', 'user', )


class QuizSessionFactAdmin(admin.ModelAdmin):
    list_display = ('quiz_session', 'fact', 'review_result', 'user', 'quiz',)
    readonly_fields = ('quiz_session', 'quiz', 'user', 'fact')


admin.site.register(Fact, FactAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizSession, QuizSessionAdmin)
admin.site.register(QuizSessionFact, QuizSessionFactAdmin)
admin.site.register(Category)
admin.site.register(Region)