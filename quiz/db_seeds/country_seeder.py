from quiz.models import Country, Region
from quiz.helpers import convert_string_to_snakecase

import logging
log = logging.getLogger(__name__)


INPUT_REGIONS = [
    "Western Europe",
    "Eastern Europe", 
    "Baltics",
    "Nordics",
    "North America",
    "Latin America", 
    "South & South-East Asia",
    "Middle East",
    "Rest of Asia",
    "Oceania", 
    "Africa",
]

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
    ["Senegal", "SN", "Africa", "Africa"]
]

OPENAI_CONTENT = {'western_europe': 'Recognizing Western European countries in GeoGuessr relies on noticing unique signage, architecture, language, and landscape. Look out for language differences, for example, French or German on signs indicating France or Germany. Distinctive architecture like Spanish balconies can point to Spain. Each country has unique road signs and vehicle license plates. Also, geographic features like mountains can hint at Alpine countries like Switzerland. Pay attention to the style of powerlines, cultivation of land, and common brands and stores.', 'eastern_europe': 'To recognize Eastern European countries in Geoguessr, look for Cyrillic or Latin alphabets on signs, as this varies by country. Architecture here can range from Soviet-era blocks to historic churches. Look for differences in language and domain endings on trucks or businesses, which can hint at the country. Vegetation can be similar across borders, but focus on vehicle license plates which often have a different background or emblem for each country.', 'baltics': "In the Baltics, focus on language on signs for a quick clue; Lithuanian and Latvian use more curved letters, like 'ā' and 'č', while Estonian aligns with Finnish. Colorful old towns with cobblestone streets are typical of the Baltics, but Tallinn is distinctly medieval. Look for the currency too; Estonia uses the euro, while Latvia and Lithuania have their own distinct currencies. Flat landscape and large forests can be seen across the region.", 'nordics': "The Nordics are recognized for their unique landscapes, languages, and distinct architectural styles. They consist of Denmark, Finland, Iceland, Norway, and Sweden. To distinguish them, focus on clues like the presence of fjords (Norway), colorful houses and old fortifications (Denmark), geothermal features (Iceland), the Finnish language signs distinct from other Nordic languages, and the red cottages in Sweden. You'll often see similarities in the overall design aesthetics and a prevalence of the Scandinavian languages, although Finnish is notably different. Watch for subtle differences in road markings, vehicle license plates, and the styles of road signs.", 'south__southeast_asia': 'Recognizing South & South-East Asian locations involves noting vegetation, architectural styles, languages on signs, and vehicle types. Dense, tropical greenery often hints at regions like Thailand or the Philippines, while arid zones suggest parts of India or Pakistan. Scooters and tuk-tuks are common on the bustling streets of Vietnam and Cambodia. Script on signage is a dead giveaway; Devanagari script points to India or Nepal, while unique characters are indicative of Thailand, Myanmar, and other regional languages. Look for national flags or emblems on government buildings and local businesses.', 'middle_east': "In the Middle East, look for Arabic script but remember, Israel uses Hebrew, and Iran uses Persian script. Notice unique architectural features like the dome and minaret in mosques. Arid landscapes are typical, but variations exist from Israel's Mediterranean coast to Iran's mountainous terrain. Pay close attention to car plates—shape, color, and symbols can hint at the specific country. Some vehicles in Israel will have yellow plates, while in Lebanon, plates are often white with a blue bar.", 'rest_of_asia': "Deciphering the 'Rest of Asia' region in GeoGuessr? Look out for unique clues like language scripts on signs, distinctive architectural styles, and local flora. Asian countries can have similarities, but scripts like Cyrillic can indicate Central Asian states, while East Asian countries will have Hanzi, Hangul, or Katakana characters. Pay attention to the landscape, vehicle designs, and even the side of the road traffic flows on. The nuances in these details will often help pinpoint the exact country.", 'oceania': 'In Oceania, look out for the diverse environments, ranging from lush rainforests to arid areas. Prominent features include island-specific architecture and often left-hand traffic flow. Road signs, local languages on signs and vehicles, and the distinct flora and fauna can be key indicators of country identification. Australia and New Zealand boast modern infrastructure while Pacific islands have more rural landscapes. Unique cultural elements and regional topography are strong hints to pinpoint the country.', 'africa': 'Distinguishing African countries in GeoGuessr can be challenging due to diverse landscapes. However, look for clues in language on signs—French in West Africa, English or Portuguese in Southern Africa. Notice driving direction: right-hand in most, left in some like South Africa. Architecture varies; northern countries have more Arabic influences, while Sub-Saharan regions have varied styles. Vegetation is key: deserts in the North, tropical forests in the Central, mixed in the South. Pay attention to car models and condition, as they can vary regionally.', 'north_america': "In North America, identifying the country can often be done by examining road signs, vehicle license plates, and architecture. The US typically has large, wide roads and highways, while Canada has bilingual signs in English and French. Mexico stands out with Spanish language signs and unique road designs. Look for flags, business names, and top-level domain hints on billboards or trucks to narrow down the location. Recognizing specific road markings, bollard designs, and the style of streetlights can also be key indicators of the country you're in.", 'latin_america': "In Geoguessr, pinpointing Latin American countries can be challenging due to their similarities. Pay attention to language - Spanish is predominant, but Brazil speaks Portuguese. Look out for distinctive road signs, vehicle license plates, and the architecture. Each country has unique elements like Colombia's yellow license plate border. Environmental clues also help; the Andes suggest western countries. Despite similarities, each nation has subtle differences in these aspects critical for location identification."}


def update_regions():
    # Create Regions
    for input_region in INPUT_REGIONS:
        region_db = Region.objects.filter(name=input_region).first()
        if region_db:
            region_db.slug = convert_string_to_snakecase(input_region)
            region_db.description = OPENAI_CONTENT[region_db.slug]
            region_db.save()
        else:
            Region.objects.create(
                name=input_region,
                slug=convert_string_to_snakecase(input_region),
                description=OPENAI_CONTENT[convert_string_to_snakecase(input_region)]
            )
        log.info(f"Region {input_region} updated")
    
    # Delete Regions
    db_regions = Region.objects.all()
    for db_region in db_regions:
        if db_region.name not in INPUT_REGIONS:
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
            country_db.save()
        else:
            Country.objects.create(
                name=input_country[0],
                iso2=input_country[1],
                continent=input_country[2],
                region=Region.objects.get(name=input_country[3]),
                slug=convert_string_to_snakecase(input_country[0]),
                region_slug=convert_string_to_snakecase(input_country[3])
            )
        log.info(f"Country {input_country[0]} updated")
    
    # Delete Countries
    input_country_names = [input_country[0] for input_country in INPUT_COUNTRIES]
    db_countries = Country.objects.all()
    for db_country in db_countries:
        if db_country.name not in input_country_names:
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
