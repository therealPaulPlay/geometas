from django import template
from quiz.models import Country
from quiz.db_seeds.country_seeder import INPUT_COUNTRIES

register = template.Library()

@register.filter(name='country_flag')
def country_flag(country_name):
    # Get country iso 2 from INPUT_COUNTRIES with is an array of arrays with name as first and iso2 as second element
    iso2 = [c[1] for c in INPUT_COUNTRIES if c[0] == country_name][0]
    return Country.get_flag_emoji(iso2)
