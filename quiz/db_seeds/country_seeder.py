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
    ["Kenya", "KE", "Africa", "Africa", False],
    ["Kyrgyzstan", "KG", "Asia", "Rest of Asia", True],
    ["Laos", "LA", "Asia", "South & South-East Asia", True],
    ["Latvia", "LV", "Europe", "Baltics", True],
    ["Lesotho", "LS", "Africa", "Africa", False],
    ["Lithuania", "LT", "Europe", "Baltics", True],
    ["Luxembourg", "LU", "Europe", "Western Europe", True],
    ["Madagascar", "MG", "Africa", "Africa", False],
    ["Malaysia", "MY", "Asia", "South & South-East Asia", False],
    ["Malta", "MT", "Europe", "Western Europe", True],
    ["Mexico", "MX", "North America", "Latin America", True],
    ["Mongolia", "MN", "Asia", "Rest of Asia", True],
    ["Montenegro", "ME", "Europe", "Eastern Europe", True],
    ["Netherlands", "NL", "Europe", "Western Europe", True],
    ["New Zealand", "NZ", "Oceania", "Oceania", False],
    ["Nigeria", "NG", "Africa", "Africa", True],
    ["North Macedonia", "MK", "Europe", "Eastern Europe", True],
    ["Northern Mariana Islands", "MP", "Oceania", "Oceania", True],
    ["Norway", "NO", "Europe", "Nordics", True],
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

OPENAI_CONTENT = {'western_europe': "In Western Europe, identifying countries via Geoguessr is an engaging puzzle. Malta, driving on the left, spells streets as 'Triq'. It's Mediterranean, unlike its left-driving peers, the UK and Ireland, which can be distinguished by unique road lines and bollards. Bollard shapes and reflectors are telltales, too; Austria's bollards are unique with black hats and reflectors. Germany has gen 4 Street View with distinctive car tinge, and peculiar white striped bollards. Swiss Italian's consistent vowel endings and low camera height set it apart. Watch for Swiss mountains, wooden houses, and CH stickers on cars. Language clues are abundant; German features umlauts, Dutch loves 'ij', and Greek uses its own alphabet. French 'rue', Italian 'via', and Spanish 'calle' all mean street. Recognizing license plates' quirks like Belgium's red text or Dutch yellow plates is helpful. Bilingual signs could hint to Brittany, and unique Belgian utility poles might be a giveaway. Spotting Switzerland might come down to window shutters and bollards, just as Andorra's stone buildings or Luxembourg's rolling terrain are signature sights.", 'eastern_europe': "To identify Eastern Europe in Geoguessr, look for distinctive signs like utility poles with concrete holes – thicker and marked in Romania, stopping before the ground in Poland. Hungarian poles are thinner and are yellow-marked on occasions. Romanian language features unique 'ş' and 'ƫ' with squiggles. Watch for the distinctive 'rift in the sky' in Montenegro and Albania. Russian bollards have a narrow support pole, while Polish bollards have red diagonal stripes. Road signs vary, from blue in Poland to yellow-black in Slovenia and Croatia, to unique shapes in Czechia. Vehicles range from right-hand steering wheels in Eastern Russia to yellow public transport plates in Ukraine and Russia. Look for the singular red car with an antenna in Ukraine. Regional variations in language, like Serbian Cyrillic's unique 'Ћ' and 'Ђ', or the exclusive use of 'Ř', 'Ě', and 'Ů' in Czech can provide clues. These details, along with specific guardrail designs, signage, and bollard types, can help pinpoint your virtual location in Eastern Europe.", 'baltics': "In the Baltics, sharp eyes can spot unique features to pinpoint your location. Latvia flaunts heftier red borders on warning signs and utility poles with 'pine cone' insulators at varied heights, facing the road. Kilometre markers in Latvia are blue, parallel to the road, while Estonia's are right-angled, and Lithuania's resemble orange-arrowed signs. Look out for Lithuanian language cues, like the 'ė' and endings in '...ai' or '...as'. Spot the distinctive bollards: thin planks in Latvia and cylindrical in Estonia, with their own white rectangle designs. Utility poles also vary, from crucifix-like in Estonia, lacking reflectors on guardrails, to 'pine cone' laden poles in Lithuania with orange reflectors. These subtle clues are key in distinguishing these neighboring nations on your next virtual journey.", 'nordics': "In the Nordics, details like license plates, road signs, and language on signs vastly help with pinpointing the exact country. Denmark has yellow plates for commercial vehicles and red-and-white directional signs. Norway boasts '...vei' or '...veien' street names and yellow directional signs. Swedish has unique 'ä' and 'ö' letters and white lines with distinctive dash-gap ratios. Finland is recognizable by Swedish/Finnish bilingual signs in the southwest, cylindrical bollards, and Finnish language double letters. Iceland's landscape is sparse with yellow and black directional signs, undulating terrain, and lack of blue on license plates. Faroe Islands stand out with their jagged green mountains and distinctive car roof racks.", 'south_southeast_asia': "Recognizing South & South-East Asia in GeoGuessr takes keen observation of unique features. Bhutanese red plates, Malaysian utility poles with black rectangles, and bollards with red rectangles are key giveaways. Distinguish languages: Hindi's upside-down 'h' and backward 'F', Khmer's right-pointing hooks, Thai's small circles, Sinhala's 'C' shapes, and Bengali's horizontal lines with left triangles. Look for the Philippines' white-outlined Street View car, Vietnam's motorbike view, or Singapore's pale green street signs. Distinctive Thai bollards and Laos' yellow plates aid identification too.", 'middle_east': 'In the Middle East, recognizing Israeli locations is made easier by identifying the unique yellow license plates with a blue vertical stripe. On the other hand, Arabic script is widespread across the region, known for its calligraphic style with lines beneath the words. Flat landscapes are indicative of the Netherlands, contrasting with Luxembourg’s slightly hilly terrain and Israel’s diverse geography. Turkey’s distinct guardrails and bollards can also be clues, while Tunisia’s black, narrow, and long license plates stand out, often seen following the Street View car.', 'rest_of_asia': "Recognizing countries in 'Rest of Asia' relies on details: Taiwan and South Korea's striped utility poles, Japan's unique yellow plates, and Korean language's distinctive circles. China, Taiwan, Hong Kong, and Macau share complicated Chinese characters, larger than Korea's blocky text and simpler than Japan's curved strokes. Kyrgyzstan can be spotted by black/white mirrors and red-striped plates. Low camera angles hint at Japan or occasionally Sri Lanka and Taiwan. Black-based utility poles suggest Russia or Kyrgyzstan, while camping-equipment undercarriages may point to Mongolia.", 'oceania': "In Oceania, distinctive markers help identify locations. Australia's flat terrain, white street signs, yellow Victorian poles, and bollards signify its vast landscapes, differing from New Zealand's red 'GIVE WAY' signs, unique silver-wrapped poles, and mountainous vistas hinting at South Island. Tasmania lures with olive wraps on poles and hilly scenery. American Samoa stands out with blue license plates and right-hand driving – a regional rarity, while Guam displays blue highway shields. Northern Mariana Islands entice with tropical palms, hilly views, and right-driving cars. Each island's nuanced cues, from bollards to street signs, aid in pinpointing your virtual whereabouts.", 'africa': "Tell-tale signs can help uncover your location within Africa. Red soil hints at locations like Uganda or Kenya, while yellow line-marked roads suggest South Africa, Botswana, Eswatini, or Lesotho. Botswana can be distinguished by black and yellow striped poles and use of 'A' and 'B' on road signs. High-quality highways and flat landscapes are typical in Botswana. Lesotho is known for its green, hilly, and treeless terrain. Rwanda stands out with high walls around properties and dual-language signage in English and Kinyarwanda. Look for bollards and narrow red and white signs as markers in South Africa, and blue license plates hinting at Senegal.", 'north_america': "North America offers distinct clues in Geoguessr. Bermuda's Street View features a black truck or a jagged blurred car. Look for uniquely bright-colored houses with striking white roofs blending with the sky. In contrast, Canadian signs have 'MAXIMUM' for speed limits and can sport a checkerboard pattern, with road signs on white-painted wooden poles. The US has 'SPEED LIMIT' signs, metal poles, and often vehicles lack a front license plate, especially in the southeast. New Brunswick uniquely showcases bilingual signs. Remember, only Bermuda drives on the left with a yellow line.", 'latin_america': "Spotting Latin America in Geoguessr? Look for signs with 'Ciudad de México' to pinpoint Mexico City. Brazil has unique transparent satellite dishes and highways labeled 'BR-XXX'. In Peru, Tuktuks and cigarette-shaped bollards are key clues. Chile's roads have uniform color lines. Puerto Rico often lacks front license plates on cars, and you'll find 'Clasificados Online' signs. Antennas under cars suggest Ecuador, while Dominicans and Mongolians have bars with thick black lines. Panama's Street View car has a unique antenna. Argentine signs and license plate blobs, along with crucifix utility poles, can be indications of Mexico or Argentina. Lastly, driving on the left is a dead giveaway for the US Virgin Islands."}


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
        log.info(f"Country {input_country[0]} updated")
    
    # Delete Countries
    input_country_names = [input_country[0] for input_country in INPUT_COUNTRIES]
    db_countries = Country.objects.all()
    for db_country in db_countries:
        if db_country.name not in input_country_names:
            if db_country.quiz:
                db_country.quiz.delete()
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
