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

OPENAI_CONTENT = {'western_europe': "Recognizing Western European countries can be tricky, but there are distinct signs. Look out for unique road features—like bollard designs, road markings like Ireland's yellow dashed lines, or Austria's black bollard reflectors. NOTICE: Gen 4 Google Street View coverage shows a blue tinge under German cars. Language hints are huge: Italian vowels, the ß character points to Germany/Austria, not Switzerland. Spot local signs: 'CALLE' in Spanish, 'rue' in French. License plate details matter; Swiss plates lack the blue EU strip. Terrain can be a clue; mountains often mean Switzerland. And don't miss subtle signs like utility poles, guardrails, and bollards unique to each location.", 'eastern_europe': "In Eastern Europe, identifying countries can be detailed work. Romania's concrete utility poles with holes and distinctive yellow marks are key identifiers, while Hungarian poles are similar but narrower. Romania, Hungary, and Poland each have unique utility poles, differing in hole placement and width. Directional signs offer clues, with Slovakia's signs featuring small white arrows and Czechia's having large arrow-shaped signs. Language is crucial, too. Romanian uses special characters like ş, ƫ, and ă. Croatian includes unique diacritics over letters. Watch for bollards and guardrails; Serbian bollards have offset red rectangles, while Czechia and Slovakia share wide central guardrail sections. Vehicle details help — Hungarian commercial vehicles often have yellow plates, while unique fire hydrants dot Croatia. Observing the details of signs, bollards, language, and road markers will enhance your Geoguessr country identification in Eastern Europe.", 'baltics': "Recognizing Baltic countries in Geoguessr? Check traffic signs: Latvia's got thicker red borders, while Lithuania's signs have a unique white border. Notice utility poles—Latvia's 'pine cone' designs vary in position. Lithuanian language is a giveaway with 'ė' and words ending in ‘...ai’ or ‘...as’. Roof styles can clue in too: Eternit for rural houses, facing the road. Kilometre markers differ; Lithuania's point to the road, Latvia's run parallel, and Estonia's are right-angled. For guardrails, Lithuania opts for orange, Latvia red and white, and Estonia skips reflectors. Utility poles again? Crucifix style likely means Estonia. Bollards distinguish too—Latvia's thin planks, Lithuania's wood-like plastics, Estonia's cylindrical. Lastly, grasp languages: Estonian has unique Õ and Ä, while Latvian showcases vowels with a horizontal line or a 'v'-like symbol above.", 'nordics': "Recognizing Nordics in Geoguessr? Look for language clues first, like Swedish 'ä' and 'ö' or Finnish double letters. Norway's undulating landscape distinguishes it, as does Iceland's volcanic, treeless terrain. Denmark has recognizable yellow plates for commercial vehicles, while Norway uses green. In Finland, watch for bilingual Swedish-Finnish signs. Spot Denmark by its unique street signs ending in '...vej' or '...gade' and specific bollard designs. Sweden's long gaps between white dashes on roads are a telltale sign. Icelandic signs avoid the typical blue European stripe, instead choosing plain white plates.", 'south_southeast_asia': "In South & South-East Asia, recognizing countries can be tricky due to regional similarities. For language, search for unique characters in scripts: hooks in Khmer for Cambodia, circles in Thai, curves in Lao, and horizontal lines in Bengali for Bangladesh. India's Hindi features inverted 'h's. Vehicle clues vary widely: red plates in Bhutan, black text blocks on Malaysian plates, yellow plates in Laos, and green/white in the Philippines. Note the street view: Vietnam has motorbike imaging, while the Philippines shows a white outline. Utility poles and bollards have distinct features: holes in Thai poles, black rectangles in Malaysia, and 'fat match' bollards in Cambodia. For signage, look for pale green signs in Singapore and blue/white/red-striped Street View cars in Sri Lanka.", 'middle_east': 'To identify Middle Eastern countries in Geoguessr, focus on language and vehicle clues. Yellow license plates with a blue strip are unique to Israel, with Hebrew text. For other countries with Arabic script, context is key; urban areas, desert landscapes, and architectural styles vary widely. Watch for specific features like the dark green Mazda in Tunisia or the white car in Qatar. Additionally, recognize regional guardrails and bollards, such as the B-profile guardrail found also in parts of Turkey.', 'rest_of_asia': 'Distinguishing Asian countries in Geoguessr, focus on unique markers. Japan features yellow license plates and pole stripes. Recognize Korean by distinct circle characters in the language. Kyrgyzstan has undercarriage bars and black/white mirrors on cars. Taiwanese utility poles are striped and distinct. Look for complex Chinese characters in China, Taiwan, Hong Kong, and Macau. Notice Japanese bollards and simpler characters. Mongolia and Sri Lanka might share lower camera angles, typically seen in Japan.', 'oceania': "Oceania road-tripping in GeoGuessr? Keep an eye out for New Zealand's distinctive bollards with red/orange stripes up top. Spotting them can confirm a Kiwi location. But if you're surrounded by tall Eucalyptus trees with white bark, chances are you've landed in Australia. These visual clues are key to differentiating the diverse landscapes down under.", 'africa': "In Africa, recognizing countries can hinge on subtle details. License plates are key: Senegal has blue ones, while some countries like Ghana boast yellow plates. Vehicle cues are vital, too; a snorkel on the Google car points to Kenya, unique aside from Mongolia. Notice the Street View car model: a silver or white truck in Senegal (Gen 4), a visible roof rack in Senegal and Ghana, and a 4-wheel drive escort in Nigeria. Road markings can tip you off, like white center lines with yellow sides in southern Africa. Look for the distinct white Street View car in South Africa, Lesotho, Eswatini, and Botswana, while it's often not visible elsewhere.", 'north_america': "North America offers diverse clues in Geoguessr. Bermuda's Street View has a distinctive black truck or a blurred vehicle, unique to the island. In the USA, 'SPEED LIMIT' signs contrast Canada's 'MAXIMUM' wording. Bermuda's houses stand out with bright yet semi-faded colors and stark white roofs, blending with the sky. Canadian road signs often use wooden poles, while the US prefers metal. Canada's black and yellow checkerboard sign is notable. The southeastern US frequently has cars without front plates. New Brunswick showcases bilingual signs, helpful to pinpoint the location. Bermuda's left-side driving and single yellow centre line on roads are key geographic hints.", 'latin_america': "In Latin America, distinct features can aid in country identification. Brazil's unique transparent satellite dishes, bulky utes in US Virgin Islands, and pink Mexico City taxis are key indicators. Chile's road lines are strictly one color. Peru's tuk-tuks, bollards, and poles, Puerto Rico's vehicle traits, Argentina and Uruguay's Street View tint, Ecuador's antenna, plus Guatemala's utility poles and distance signs all provide country-specific clues. Recognize Mexico by octagonal poles, 'ALTO' stop signs, large water tanks, and circular electricity meters. Always check for driving side and license plate styles to narrow down your location."}


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
            if db_country.quiz:
                db_country.quiz.delete()
            db_country.delete()
            log.info(f"Country {db_country.name} deleted")
