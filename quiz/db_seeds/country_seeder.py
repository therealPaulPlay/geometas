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
    ["Greenland", "GL", "North America", "Nordics"],
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

OPENAI_CONTENT = {'western_europe': "Western Europe offers a mix of subtle clues for GeoGuessr players. Distinguish Ireland by its yellow dashed line and Austria by black or dark red bollards. German Street View often shows a blue car, while Italian signs end with vowels. Cars drive on the left only in the UK, Ireland, and Malta. French roads have distinctive 'D' roads and long white dash markings. Belgium license plates have red text, and its utility poles have small holes. Town direction signs in Portugal have a blue base and a yellow stripe on license plates. Spain's speed signs uniquely fill the sides with red and have yellow-orange guardrail reflectors. Dutch signs often use 'weg' or 'straat' and have blue directional arrows. Brittany has bilingual signs, and Andorra's buildings are distinctively stony with multi-storey structures. Look for the yellow diamond signs in Ireland and the urban bilingual signs in Belgium for confirmation of location.", 'eastern_europe': "Identifying Eastern Europe in GeoGuessr? Look for unique alphabets; Č, Š, Ž are exclusive to Czechia, Ľ, Ô, Ä to Slovakia. Russian bollards have a narrow support pole, while Ukrainian versions appear run-down. Poland's road signs have thin borders; utility poles' holes don't reach the ground. Romania and Hungary share concrete utility pole designs. Note Serbia's asymmetric red rectangles on bollards. Russian roads have M, A, P/R prefixes, and Ukraine's license plates have hints of national colors. Spotting these details sharpens your geo-sleuth skills!", 'baltics': "Spotting countries in the Baltics can be tricky, but bollards offer a clue. Estonian bollards are cylindrical with unique markings: a white rectangle encased in black at the front, sometimes yellow, and two white circles at the back. Latvian bollards differ; they're thin planks with white rectangles at the front and two white circles on the rear. Meanwhile, Lithuanian bollards stand out with a white rectangle on the rear and distinctive plastic with an orange rectangle at the front, mimicking wood. These differences are key to pinpointing the exact Baltic country.", 'nordics': "Recognizing Nordic countries in Geoguessr revolves around key details. Denmark has distinct short-dashed road markings and yellow commercial plates. Norwegian roads often have elongated white dashed markings, plus unique signs in Norwegian and Sami up north. Sweden's white road dashes have longer gaps, and you might spot the Swedish language's characteristic 'ä' and 'ö' letters. Finland features bilingual signs in the south-west and doubled letters in Finnish. Icelandic landscapes are hillier with limited vegetation, and you'll notice unique yellow bollards and pedestrian signs without a blue EU strip. Also, Faroe Islands reveal themselves by jagged landscapes and grey roof racks on cars.", 'south_southeast_asia': "In South & South-East Asia, identifying countries from Street View clues means paying attention to details. Bhutan's cars flaunt unique red plates, while Malaysia shows black rectangles on poles—an exclusive mainland feature. Languages offer clues, like Hindi's distinctive 'h' in India and Khmer's right-pointing hooks in Cambodia. Philippine Street Views often reveal white car outlines. Bollard shapes differ: red-topped in Malaysia, match-like in Cambodia, and striped obelisk-style in Thailand. Spot Laos by yellow plates and curved letters in the script. Utility poles in Thailand have tell-tale vertical holes. Singapore's pale green street signs stand out, while Sri Lanka's Sinhala script features ‘C’ shaped letters. Language differentiation is key: Thai uses circles, Lao curves, and Bengali lines with left-pointing triangles.", 'middle_east': "Recognizing Middle Eastern countries in Geoguessr hinges on observing distinct features. License plates are key, with Israel having distinct yellow plates with a blue stripe, compared to Tunisia's black long plates. Language cues are crucial; Hebrew is unique to Israel, while Arabic script's calligraphic lines are seen across the region. Watch for certain vehicles, like the dark green Mazda in Tunisia or the white car in Qatar. Turkey's bollards, resembling Australia's and Netherlands', are broader. Landscape-wise, Israel's terrain contrasts with the flat Netherlands and Luxembourg's more varied topography.", 'rest_of_asia': "In the vast region of 'Rest of Asia', picking up visual clues is crucial. Yellow plates are a telltale sign of Japan, but look out for their unique writing style with simpler curved strokes like ノ and シ. Korea's Hangul script stands out with its blocky appearance and characteristic circles, while Chinese characters are more complex with extra strokes. Kyrgyzstan can be identified by black/white side mirrors and a red stripe on license plates. Utility poles offer hints too; Taiwan's are striped black and yellow, a pattern also common in South Korea. Mongolia features distinctive equipment under Street View cars. Keep these details in mind to pinpoint your location successfully.", 'oceania': "Recognizing Oceania in GeoGuessr hinges on subtle details. New Zealand has distinct highway bollards with red/orange strips. Spotting these can confirm your location. Australia's telltale signs include Eucalyptus trees, often tall with white bark, indicative of the Aussie landscape. Both features are unique identifiers within the Oceania region.", 'africa': "Recognizing African countries in Geoguessr includes looking at road markings, vehicles, and license plates. Yellow center lines with white edges suggest South Africa, Botswana, Eswatini, or Lesotho. Blue license plates might point to Senegal, where you could also spot a silver or white truck in Gen 4 or a roof-racked Gen 3 car. Ghana's Google car also has a roof rack with distinctive black tape. Kenya is notable for a snorkel on the Street View car. In South Africa, prominent red and white roadside bollards are a giveaway. Black escort vehicles hint at Nigeria, while Uganda features white edges on the Street View car. These nuances are key to pinpointing your virtual location.", 'north_america': "Identifying locations in North America can be done via unique local features. Look for language on road signs, with Canada often featuring bilingual signs and distinctive terms like 'MAXIMUM' for speed limits, contrasting the U.S. 'SPEED LIMIT'. Canadian signs might be mounted on wooden poles, and you can spot unique checkerboard signs. Pay attention to vehicle traits; cars without a front plate suggest southeastern U.S. regions. In Bermuda, you'll spot houses with vibrant, semi-faded colors and stark white roofs, a black truck or a jagged blurred car on Street View, and remember they drive on the left with a singular yellow line on roads.", 'latin_america': "In Latin America, unique signs and vehicles can guide you. Mexico's pink taxis and octagonal poles, Chile's uniform road lines, and Puerto Rico's classified ads are key indicators. Tuktuks hint at Peru, and the US Virgin Islands' left-side driving stands out. Specific items like Brazil's BR highways, Guatemalan bars, and Colombian yellow plates sharpen your guesses. Notice the small details like bollards, utility poles, and antenna shapes to pinpoint locations."}


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
            country_db.save()
        else:
            Country.objects.create(
                name=input_country[0],
                iso2=input_country[1],
                continent=input_country[2],
                region=Region.objects.get(name=input_country[3]),
                slug=convert_string_to_snakecase(input_country[0])
            )
        log.info(f"Country {input_country[0]} updated")
    
    # Delete Countries
    input_country_names = [input_country[0] for input_country in INPUT_COUNTRIES]
    db_countries = Country.objects.all()
    for db_country in db_countries:
        if db_country.name not in input_country_names:
            db_country.quiz.delete()
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
