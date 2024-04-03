from quiz.models import Country, Region
from quiz.helpers import convert_string_to_snakecase
from quiz.db_seeds.openai_content import OPENAI_REGIONS

import logging
log = logging.getLogger(__name__)


INPUT_REGIONS = [
    ["Western Europe", 1],
    ["Eastern Europe",  2],
    ["Baltics", 4],
    ["Nordics", 3],
    ["North America", 6],
    ["Latin America",  5],
    ["South & South-East Asia", 7],
    ["Middle East", 11],
    ["Rest of Asia", 8],
    ["Oceania",  9],
    ["Africa", 10],
]

INPUT_COUNTRIES = [
    ["Albania", "AL", "Europe", "Eastern Europe", True],
    ["American Samoa", "AS", "Oceania", "Oceania", False],
    ["Andorra", "AD", "Europe", "Western Europe", True],
    ["Argentina", "AR", "South America", "Latin America", True],
    ["Australia", "AU", "Oceania", "Oceania", False],
    ["Austria", "AT", "Europe", "Western Europe", True],
    ["Bangladesh", "BD", "Asia", "South & South-East Asia", False],
    ["Belgium", "BE", "Europe", "Western Europe", True],
    ["Bermuda", "BM", "North America", "North America", True],
    ["Bhutan", "BT", "Asia", "South & South-East Asia", False],
    ["Bolivia", "BO", "South America", "Latin America", True],
    ["Brazil", "BR", "South America", "Latin America", True],
    ["Botswana", "BW", "Africa", "Africa", False],
    ["Bulgaria", "BG", "Europe", "Eastern Europe", True],
    ["Cambodia", "KH", "Asia", "South & South-East Asia", True],
    ["Canada", "CA", "North America", "North America", True],
    ["Chile", "CL", "South America", "Latin America", True],
    ["China", "CN", "Asia", "Rest of Asia", True],
    ["Christmas Island", "CX", "Asia", "South & South-East Asia", True],
    ["Colombia", "CO", "South America", "Latin America", True],
    ["Costa Rica", "CR", "North America", "Latin America", True],
    ["Croatia", "HR", "Europe", "Eastern Europe", True],
    ["Curaçao", "CW", "South America", "Latin America", True],
    ["Czech Republic", "CZ", "Europe", "Eastern Europe", True],
    ["Denmark", "DK", "Europe", "Nordics", True],
    ["Dominican Republic", "DO", "South America", "Latin America", True],
    ["Ecuador", "EC", "South America", "Latin America", True],
    ["Estonia", "EE", "Europe", "Baltics", True],
    ["Eswatini", "SZ", "Africa", "Africa", False],
    ["Faroe Islands", "FO", "Europe", "Nordics", True],
    ["Finland", "FI", "Europe", "Nordics", True],
    ["France", "FR", "Europe", "Western Europe", True],
    ["Germany", "DE", "Europe", "Western Europe", True],
    ["Ghana", "GH", "Africa", "Africa", True],
    ["Greece", "GR", "Europe", "Western Europe", True],
    ["Greenland", "GL", "Europe", "Nordics", True],
    ["Guam", "GU", "Oceania", "Oceania", True],
    ["Guatemala", "GT", "North America", "Latin America", True],
    ["Hong Kong", "HK", "Asia", "Rest of Asia", False],
    ["Hungary", "HU", "Europe", "Eastern Europe", True],
    ["Iceland", "IS", "Europe", "Nordics", True],
    ["India", "IN", "Asia", "South & South-East Asia", False],
    ["Indonesia", "ID", "Asia", "South & South-East Asia", False],
    ["Ireland", "IE", "Europe", "Western Europe", False],
    ["Isle of Man", "IM", "Europe", "Western Europe", False],
    ["Israel", "IL", "Asia", "Middle East", True],
    ["Italy", "IT", "Europe", "Western Europe", True],
    ["Japan", "JP", "Asia", "Rest of Asia", False],
    ["Jordan", "JO", "Asia", "Middle East", True],
    ["Kazakhstan", "KE", "Africa", "Rest of Asia", True],
    ["Kenya", "KZ", "Asia", "Africa", False],
    ["Kyrgyzstan", "KG", "Asia", "Rest of Asia", True],
    ["Laos", "LA", "Asia", "South & South-East Asia", True],
    ["Latvia", "LV", "Europe", "Baltics", True],
    ["Lesotho", "LS", "Africa", "Africa", False],
    ["Lithuania", "LT", "Europe", "Baltics", True],
    ["Luxembourg", "LU", "Europe", "Western Europe", True],
    ["Madagascar", "MG", "Africa", "Africa", False],
    ["Malaysia", "MY", "Asia", "South & South-East Asia", False],
    ["Malta", "MT", "Europe", "Western Europe", False],
    ["Mexico", "MX", "North America", "Latin America", True],
    ["Monaco", "MC", "Europe", "Western Europe", True],
    ["Mongolia", "MN", "Asia", "Rest of Asia", True],
    ["Montenegro", "ME", "Europe", "Eastern Europe", True],
    ["Netherlands", "NL", "Europe", "Western Europe", True],
    ["New Zealand", "NZ", "Oceania", "Oceania", False],
    ["Nigeria", "NG", "Africa", "Africa", True],
    ["North Macedonia", "MK", "Europe", "Eastern Europe", True],
    ["Northern Mariana Islands", "MP", "Oceania", "Oceania", True],
    ["Norway", "NO", "Europe", "Nordics", True],
    ["Pakistan", "PK", "Asia", "South & South-East Asia", False],
    ["Palestine", "PS", "Asia", "Middle East", True],
    ["Panama", "PA", "North America", "Latin America", True],
    ["Peru", "PE", "South America", "Latin America", True],
    ["Philippines", "PH", "Asia", "South & South-East Asia", True],
    ["Poland", "PL", "Europe", "Eastern Europe", True],
    ["Portugal", "PT", "Europe", "Western Europe", True],
    ["Puerto Rico", "PR", "North America", "Latin America", True],
    ["Qatar", "QA", "Asia", "Middle East", True],
    ["Réunion", "RE", "Africa", "Africa", True],
    ["Romania", "RO", "Europe", "Eastern Europe", True],
    ["Russia", "RU", "Europe", "Eastern Europe", True],
    ["Rwanda", "RW", "Africa", "Africa", True],
    ["Senegal", "SN", "Africa", "Africa", True],
    ["Serbia", "RS", "Europe", "Eastern Europe", True],
    ["Singapore", "SG", "Asia", "South & South-East Asia", False],
    ["Slovakia", "SK", "Europe", "Eastern Europe", True],
    ["Slovenia", "SI", "Europe", "Eastern Europe", True],
    ["South Africa", "ZA", "Africa", "Africa", False],
    ["South Korea", "KR", "Asia", "Rest of Asia", True],
    ["Sri Lanka", "LK","Asia", "South & South-East Asia", False],
    ["Spain", "ES", "Europe", "Western Europe", True],
    ["Sweden", "SE", "Europe", "Nordics", True],
    ["Switzerland", "CH", "Europe", "Western Europe", True],
    ["Taiwan", "TW", "Asia", "Rest of Asia", True],
    ["Thailand", "TH", "Asia", "South & South-East Asia", False],
    ["Tunisia", "TN", "Asia", "Middle East", True],
    ["Turkey", "TR", "Asia", "Middle East", True],
    ["Uganda", "UG", "Africa", "Africa", False],
    ["Ukraine", "UA", "Europe", "Eastern Europe", True],
    ["U.S. Minor Outlying Islands", "UM", "Oceania", "Oceania", True],
    ["U.S. Virgin Islands", "VI", "North America", "Latin America", False],
    ["United Arab Emirates (UAE)", "AE", "Asia", "Middle East", True],
    ["United Kingdom (UK)", "GB", "Europe", "Western Europe", False],
    ["United States of America (USA)", "US", "North America", "North America", True],
    ["Uruguay", "UY", "South America", "Latin America", True],
    ["Vietnam", "VN", "Asia", "South & South-East Asia", True],
]


def update_regions():
    # Create Regions
    for input_region in INPUT_REGIONS:
        region_name = input_region[0]
        region_sort_order = input_region[1]
        region_db = Region.objects.filter(name=region_name).first()
        if region_db:
            region_db.slug = convert_string_to_snakecase(region_name)
            region_db.description = OPENAI_REGIONS[region_db.slug]
            region_db.sort_order = region_sort_order
            region_db.save()
        else:
            Region.objects.create(
                name=region_name,
                slug=convert_string_to_snakecase(region_name),
                description=OPENAI_REGIONS[convert_string_to_snakecase(region_name)],
                sort_order=region_sort_order
            )
            log.info(f"Region {region_name} created")
    
    # Delete Regions
    db_regions = Region.objects.all()
    region_names = [input_region[0] for input_region in INPUT_REGIONS]
    for db_region in db_regions:
        if db_region.name not in region_names:
            if db_region.quiz:
                db_region.quiz.delete()
            db_region.delete()
            log.info(f"Region {db_region.name} deleted")



def update_countries():
    # Create regions
    update_regions()

    # Create Countrys
    for input_country in INPUT_COUNTRIES:
        country_db = Country.objects.filter(name=input_country[0]).first()
        if country_db:
            country_db.slug = convert_string_to_snakecase(input_country[0])
            country_db.iso2 = input_country[1]
            country_db.continent = input_country[2]
            country_db.region = Region.objects.get(name=input_country[3])
            country_db.right_hand_traffic = input_country[4]
            country_db.save()
        else:
            Country.objects.create(
                name=input_country[0],
                iso2=input_country[1],
                continent=input_country[2],
                region=Region.objects.get(name=input_country[3]),
                slug=convert_string_to_snakecase(input_country[0]),
                right_hand_traffic=input_country[4]
            )
            log.info(f"Country {input_country[0]} created")
    
    # Delete Countries
    input_country_names = [input_country[0] for input_country in INPUT_COUNTRIES]
    db_countries = Country.objects.all()
    for db_country in db_countries:
        if db_country.name not in input_country_names:
            if db_country.quiz:
                db_country.quiz.delete()
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
