from quiz.models import Country
from quiz.helpers import convert_string_to_snakecase

import logging
log = logging.getLogger(__name__)

"""
from quiz.country_seeder import update_countries
update_countries()
"""

INPUT_COUNTRIES = [
    ["Albania", "AL", "Europe", "Eastern Europe"],
    ["Andorra", "AS", "Europe", "Western Europe"],
    ["Argentina", "AR", "South America", "Latin America"],
    ["Australia", "AU", "Oceania", "Oceania"],
    ["Austria", "AT", "Europe", "Western Europe"],
    ["Bangladesh", "BD", "Asia", "South & South-East Asia"],
    ["Belgium", "BE", "Europe", "Western Europe"],
    ["Bermuda", "BM", "North America", "North America"],
    ["Bhutan", "BT", "Asia", "South & South-East Asia"],
    ["Brazil", "BR", "South America", "Latin America"],
    ["Botswana", "BW", "Africa", "Africa"],
    ["Bulgaria", "BG", "Europe", "Eastern Europe"],
    ["Cambodia", "KH", "Asia", "South & South-East Asia"],
    ["Canada", "CA", "North America", "North America"],
    ["Chile", "CL", "South America", "Latin America"],
    ["China", "CN", "Asia", "Rest of Asia"],
    ["Colombia", "CO", "South America", "Latin America"],
    ["Costa Rica", "CR", "North America", "Latin America"],
    ["Croatia", "HR", "Europe", "Eastern Europe"],
    ["Czech Republic", "CZ", "Europe", "Eastern Europe"],
    ["Denmark", "DK", "Europe", "Nordics"],
    ["Dominican Republic", "DO", "South America", "Latin America"],
    ["Ecuador", "EC", "South America", "Latin America"],
    ["Estonia", "EE", "Europe", "Baltics"],
    ["Eswatini", "SZ", "Africa", "Africa"],
    ["Faroe Islands", "FO", "Europe", "Nordics"],
    ["Finland", "FI", "Europe", "Nordics"],
    ["France", "FR", "Europe", "Western Europe"],
    ["Germany", "DE", "Europe", "Western Europe"],
    ["Greece", "GR", "Europe", "Western Europe"],
    ["Guatemala", "GT", "North America", "Latin America"],
    ["Hungary", "HU", "Europe", "Eastern Europe"],
    ["Iceland", "IS", "Europe", "Nordics"],
    ["India", "IN", "Asia", "South & South-East Asia"],
    ["Indonesia", "ID", "Asia", "South & South-East Asia"],
    ["Ireland", "IE", "Europe", "Western Europe"],
    ["Isle of Man", "IM", "Europe", "Western Europe"],
    ["Israel", "IL", "Asia", "Middle East"],
    ["Italy", "IT", "Europe", "Western Europe"],
    ["Japan", "JP", "Asia", "Rest of Asia"],
    ["Jordan", "JO", "Asia", "Middle East"],
    ["Kyrgyzstan", "KG", "Asia", "Rest of Asia"],
    ["Laos", "LA", "Asia", "South & South-East Asia"],
    ["Latvia", "LV", "Europe", "Baltics"],
    ["Lesotho", "LS", "Africa", "Africa"],
    ["Lithuania", "LT", "Europe", "Baltics"],
    ["Luxembourg", "LU", "Europe", "Western Europe"],
    ["Malaysia", "MY", "Asia", "South & South-East Asia"],
    ["Malta", "MT", "Europe", "Western Europe"],
    ["Mexico", "MX", "North America", "Latin America"],
    ["Mongolia", "MN", "Asia", "Rest of Asia"],
    ["Montenegro", "ME", "Europe", "Eastern Europe"],
    ["Netherlands", "NL", "Europe", "Western Europe"],
    ["New Zealand", "NZ", "Oceania", "Oceania"],
    ["Nigeria", "NG", "Africa", "Africa"],
    ["North Macedonia", "MK", "Europe", "Eastern Europe"],
    ["Norway", "NO", "Europe", "Nordics"],
    ["Panama", "PA", "North America", "Latin America"],
    ["Peru", "PE", "South America", "Latin America"],
    ["Philippines", "PH", "Asia", "South & South-East Asia"],
    ["Poland", "PL", "Europe", "Eastern Europe"],
    ["Portugal", "PT", "Europe", "Western Europe"],
    ["Puerto Rico", "PR", "North America", "Latin America"],
    ["Qatar", "QA", "Asia", "Middle East"],
    ["Romania", "RO", "Europe", "Eastern Europe"],
    ["Russia", "RU", "Europe", "Eastern Europe"],
    ["Rwanda", "RW", "Africa", "Africa"],
    ["Serbia", "RS", "Europe", "Eastern Europe"],
    ["Singapore", "SG", "Asia", "South & South-East Asia"],
    ["Slovakia", "SK", "Europe", "Eastern Europe"],
    ["Slovenia", "SI", "Europe", "Eastern Europe"],
    ["South Africa", "ZA", "Africa", "Africa"],
    ["South Korea", "KR", "Asia", "Rest of Asia"],
    ["Sri Lanka", "LK","Asia", "South & South-East Asia"],
    ["Spain", "ES", "Europe", "Western Europe"],
    ["Sweden", "SE", "Europe", "Nordics"],
    ["Switzerland", "CH", "Europe", "Western Europe"],
    ["Taiwan", "TW", "Asia", "Rest of Asia"],
    ["Thailand", "TH", "Asia", "South & South-East Asia"],
    ["Tunisia", "TN", "Africa", "Middle East"],
    ["Turkey", "TR", "Asia", "Middle East"],
    ["Uganda", "UG", "Africa", "Africa"],
    ["Ukraine", "UA", "Europe", "Eastern Europe"],
    ["U.S. Virgin Islands", "VI", "North America", "Latin America"],
    ["United Arab Emirates (UAE)", "AE", "Asia", "Middle East"],
    ["United Kingdom (UK)", "GB", "Europe", "Western Europe"],
    ["United States of America (USA)", "US", "North America", "North America"],
    ["Uruguay", "UY", "South America", "Latin America"],
    ["Vatican City", "VA", "Europe", "Western Europe"],
    ["Vietnam", "VN", "Asia", "South & South-East Asia"],
    ["Ghana", "GH", "Africa", "Africa"],
    ["Kenya", "KE", "Africa", "Africa"],
    ["Senegal", "SN", "Africa", "Africa"],
    ["World", "__", "", ""]
]



def update_countries():
    for input_country in INPUT_COUNTRIES:
        country_db = Country.objects.filter(name=input_country[0]).first()
        if country_db:
            country_db.slug = convert_string_to_snakecase(input_country[0])
            country_db.iso2 = input_country[1]
            country_db.continent = input_country[2]
            country_db.region = input_country[3]
            country_db.region_slug = convert_string_to_snakecase(input_country[3])
            country_db.save()
        else:
            Country.objects.create(
                name=input_country[0],
                iso2=input_country[1],
                continent=input_country[2],
                region=input_country[3],
                slug=convert_string_to_snakecase(input_country[0]),
                region_slug=convert_string_to_snakecase(input_country[3])
            )
        log.info(f"Country {input_country[0]} updated")
    
    # Run through DB countries to see if we need to delete any
    input_country_names = [input_country[0] for input_country in INPUT_COUNTRIES]
    db_countries = Country.objects.all()
    for db_country in db_countries:
        if db_country.name not in input_country_names:
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
        