from quiz.models import Country

import logging
log = logging.getLogger(__name__)

"""
from quiz.country_seeder import update_countries
update_countries()
"""

INPUT_COUNTRIES = [
    ["Argentina", "AR", "South America"],
    ["Australia", "AU", "Oceania"],
    ["Austria", "AT", "Europe"],
    ["Belgium", "BE", "Europe"],
    ["Brazil", "BR", "South America"],
    ["Bolivia", "BO", "South America"],
    ["Bulgaria", "BG", "Europe"],
    ["Canada", "CA", "North America"],
    ["Chile", "CL", "South America"],
    ["Colombia", "CO", "South America"],
    ["Croatia", "HR", "Europe"],
    ["Czech Republic", "CZ", "Europe"],
    ["Denmark", "DK", "Europe"],
    ["Estonia", "EE", "Europe"],
    ["Finland", "FI", "Europe"],
    ["France", "FR", "Europe"],
    ["Germany", "DE", "Europe"],
    ["Greece", "GR", "Europe"],
    ["Hungary", "HU", "Europe"],
    ["Iceland", "IS", "Europe"],
    ["India", "IN", "Asia"],
    ["Indonesia", "ID", "Asia"],
    ["Ireland", "IE", "Europe"],
    ["Italy", "IT", "Europe"],
    ["Japan", "JP", "Asia"],
    ["Laos", "LA", "Asia"],
    ["Latvia", "LV", "Europe"],
    ["Lithuania", "LT", "Europe"],
    ["Luxembourg", "LU", "Europe"],
    ["Malaysia", "MY", "Asia"],
    ["Mexico", "MX", "North America"],
    ["Netherlands", "NL", "Europe"],
    ["New Zealand", "NZ", "Oceania"],
    ["Norway", "NO", "Europe"],
    ["Peru", "PE", "South America"],
    ["Philippines", "PH", "Asia"],
    ["Poland", "PL", "Europe"],
    ["Portugal", "PT", "Europe"],
    ["Romania", "RO", "Europe"],
    ["Russia", "RU", "Europe"],
    ["Serbia", "RS", "Europe"],
    ["Singapore", "SG", "Asia"],
    ["Slovakia", "SK", "Europe"],
    ["Slovenia", "SI", "Europe"],
    ["South Africa", "ZA", "Africa"],
    ["South Korea", "KR", "Asia"],
    ["Spain", "ES", "Europe"],
    ["Sweden", "SE", "Europe"],
    ["Switzerland", "CH", "Europe"],
    ["Taiwan", "TW", "Asia"],
    ["Thailand", "TH", "Asia"],
    ["Turkey", "TR", "Asia"],
    ["Ukraine", "UA", "Europe"],
    ["United Kingdom", "GB", "Europe"],
    ["United States", "US", "North America"],
    ["Uruguay", "UY", "South America"],
    ["Vatican City", "VA", "Europe"],
    ["Ghana", "GH", "Africa"],
    ["Kenya", "KE", "Africa"],
    ["Senegal", "SN", "Africa"],
    ["World", "ALL", ""],
    ["Cambodia", "KH", "Asia"],
    ["Botswana", "", "Africa"],
    ["Eswatini", "", "Africa"],
    ["Lesotho", "", "Africa"],
    ["Faroe Islands", "FO", "Europe"],
    ["Andorra", "", "Europe"],
    ["Montenegro", "ME", "Europe"],
    ["North Macedonia", "MK", "Europe"]
]



def update_countries():
    for input_country in INPUT_COUNTRIES:
        country_db = Country.objects.filter(name=input_country[0]).first()
        if country_db:
            country_db.iso2 = input_country[1]
            country_db.continent = input_country[2]
            country_db.save()
        else:
            Country.objects.create(
                name=input_country[0],
                iso2=input_country[1],
                continent=input_country[2]
            )
        log.info(f"Country {input_country[0]} updated")
        