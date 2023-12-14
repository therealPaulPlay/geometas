from quiz.models import Country

import logging
log = logging.getLogger(__name__)

"""
from quiz.country_seeder import update_countries
update_countries()
"""

INPUT_COUNTRIES = [
    ["Albania", "AL", "Europe"],
    ["Andorra", "AS", "Europe"],
    ["Argentina", "AR", "South America"],
    ["Australia", "AU", "Oceania"],
    ["Austria", "AT", "Europe"],
    ["Belgium", "BE", "Europe"],
    ["Bhutan", "BT", "Asia"],
    ["Brazil", "BR", "South America"],
    ["Bolivia", "BO", "South America"],
    ["Botswana", "BW", "Africa"],
    ["Bulgaria", "BG", "Europe"],
    ["Cambodia", "KH", "Asia"],
    ["Canada", "CA", "North America"],
    ["Chile", "CL", "South America"],
    ["Colombia", "CO", "South America"],
    ["Croatia", "HR", "Europe"],
    ["Czech Republic", "CZ", "Europe"],
    ["Denmark", "DK", "Europe"],
    ["Dominican Republic", "DO", "South America"],
    ["Ecuador", "EC", "South America"],
    ["Estonia", "EE", "Europe"],
    ["Eswatini", "SW", "Africa"],
    ["Faroe Islands", "FO", "Europe"],
    ["Finland", "FI", "Europe"],
    ["France", "FR", "Europe"],
    ["Germany", "DE", "Europe"],
    ["Greece", "GR", "Europe"],
    ["Guatemala", "GT", "North America"],
    ["Hungary", "HU", "Europe"],
    ["Iceland", "IS", "Europe"],
    ["India", "IN", "Asia"],
    ["Indonesia", "ID", "Asia"],
    ["Ireland", "IE", "Europe"],
    ["Isle of Man", "IM", "Europe"],
    ["Italy", "IT", "Europe"],
    ["Japan", "JP", "Asia"],
    ["Kyrgyzstan", "KG", "Asia"],
    ["Laos", "LA", "Asia"],
    ["Latvia", "LV", "Europe"],
    ["Lesotho", "LS", "Africa"],
    ["Lithuania", "LT", "Europe"],
    ["Luxembourg", "LU", "Europe"],
    ["Malaysia", "MY", "Asia"],
    ["Mexico", "MX", "North America"],
    ["Mongolia", "MN", "Asia"],
    ["Montenegro", "ME", "Europe"],
    ["Netherlands", "NL", "Europe"],
    ["New Zealand", "NZ", "Oceania"],
    ["North Macedonia", "MK", "Europe"]
    ["Norway", "NO", "Europe"],
    ["Peru", "PE", "South America"],
    ["Philippines", "PH", "Asia"],
    ["Poland", "PL", "Europe"],
    ["Portugal", "PT", "Europe"],
    ["Qatar", "QA", "Asia"],
    ["Romania", "RO", "Europe"],
    ["Russia", "RU", "Europe"],
    ["Rwanda", "RW", "Africa"],
    ["Serbia", "RS", "Europe"],
    ["Singapore", "SG", "Asia"],
    ["Slovakia", "SK", "Europe"],
    ["Slovenia", "SI", "Europe"],
    ["South Africa", "ZA", "Africa"],
    ["South Korea", "KR", "Asia"],
    ["Sri Lanka", "LK","Asia"],
    ["Spain", "ES", "Europe"],
    ["Sweden", "SE", "Europe"],
    ["Switzerland", "CH", "Europe"],
    ["Taiwan", "TW", "Asia"],
    ["Thailand", "TH", "Asia"],
    ["Tunisia", "TN", "Africa"],
    ["Turkey", "TR", "Asia"],
    ["Ukraine", "UA", "Europe"],
    ["U.S. Virgin Islands", "VI", "North America"],
    ["United Kingdom", "GB", "Europe"],
    ["United States", "US", "North America"],
    ["Uruguay", "UY", "South America"],
    ["Vatican City", "VA", "Europe"],
    ["Vietnam", "VN", "Asia"],
    ["Ghana", "GH", "Africa"],
    ["Kenya", "KE", "Africa"],
    ["Senegal", "SN", "Africa"],
    ["World", "ALL", ""],   
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
        