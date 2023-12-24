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
    ["Greenland", "GL", "Europe", "Nordics"],
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
    ["Tunisia", "TN", "Asia", "Middle East"],
    ["Turkey", "TR", "Asia", "Middle East"],
    ["Uganda", "UG", "Africa", "Africa"],
    ["Ukraine", "UA", "Europe", "Eastern Europe"],
    ["U.S. Virgin Islands", "VI", "North America", "Latin America"],
    ["United Arab Emirates (UAE)", "AE", "Asia", "Middle East"],
    ["United Kingdom (UK)", "GB", "Europe", "Western Europe"],
    ["United States of America (USA)", "US", "North America", "North America"],
    ["Uruguay", "UY", "South America", "Latin America"],
    ["Vietnam", "VN", "Asia", "South & South-East Asia"],
    ["Ghana", "GH", "Africa", "Africa"],
    ["Kenya", "KE", "Africa", "Africa"],
    ["Senegal", "SN", "Africa", "Africa"],
    ["Northern Mariana Islands", "MP", "Oceania", "Oceania"],
    ["Guam", "GU", "Oceania", "Oceania"],
    ["Christmas Island", "CX", "Asia", "South & South-East Asia"],
    ["American Samoa", "AS", "Oceania", "Oceania"],
]

OPENAI_CONTENT = {'western_europe': "Western Europe is eclectic in driving patterns, languages, and road markers. Malta's leftside driving is unique beside the UK and Ireland. Austria's bollards with dark reflectors stand out. Germany's Gen 4 Street View gives a blue car tinge. Swiss and Japanese low camera height is telling. Belgian distinct plates, license plate colors in Andorra, Portugal's yellow stripe on plates, Spain's unique road signs, and the Dutch language's repetitive letters are notable. Look for French 'rue', Italian word endings in vowels, and Swiss 'CH' stickers. Guardrail types can reveal the country, as can specific bollard designs in Italy and Austria. Spot locales by their language traits, license plates, and road sign colors or shapes.", 'eastern_europe': 'Recognizing Eastern European countries in Geoguessr involves looking out for unique environmental clues. For instance, Romanian concrete utility poles are thick, with distinctive holes and often a yellow mark. Hungarian, Polish, and Ukrainian poles have different features like varying hole placement or paint. Language signs also provide big hints; for example, Romanian has special characters like ş and ă, while unique letters are present in Polish and Croatian. Check for driving side in Russia as Eastern Russia mostly features right-hand drive vehicles. Guardrails, street signs, and bollards can also vary by country, with specific shapes and colors. Look for regional nuances such as specific paint or shapes on fire hydrants in Hungary and Croatia. License plates can be a giveaway, with variations in color and layout, so observe them closely alongside road signage that often includes language-specific alphabets like Cyrillic in Bulgaria and Montenegro.', 'baltics': "Recognizing the Baltics in Geoguessr hinges on small details. Look for thicker red borders on Latvian warning signs, and pine cone-like features on Latvian utility poles at varied heights. Lithuanian language clues include the unique ė and words ending in 'ai' or 'as'. For roofs, seek the eternit style facing roads. Guardrail reflectors also vary: Lithuania has orange, Latvia has red and white, and Estonia has none. Latvian blue kilometre markers face the road, whereas Estonian markers are perpendicular, and Lithuanian markers point arrow-like. Lastly, Latvia's language features a horizontal line above certain vowels such as ā, ē, ī, ō, ū, and Estonian utility poles might resemble crucifixes. These nuances will guide you through the Baltic landscapes.", 'nordics': "In the Nordics, unique features help distinguish countries in Geoguessr. Denmark has yellow plates for commercial vehicles and blue/white European plates for others. Norway and Denmark feature distinct road signs. Finnish signs include Swedish due to the bilingual region. Iceland's landscape is grassy with volcanic and glacial features. Faroe Islands show jagged green landscapes and distinct vehicles. Bollards' shapes, road lines, and language hints like double letters and unique symbols (like æ, ø, å) also provide clues. Local suffixes for street names vary by country. Language-specific letters and sign colors can be vital identifiers, as can the distinctiveness of the terrain and the presence of certain natural features.", 'south_southeast_asia': "Recognize South & South-East Asia in Geoguessr by details like language scripts, vehicle details, and infrastructure nuances. Spot unique red plates in Bhutan or look for Hindi's distinctive 'upside-down h' and backwards 'F' in India. Khmer in Cambodia features rightward hooks on symbols, unlike Thai's small circles. In Malaysia, notice bollards with red rectangles and black-and-white utility pole labels. Catch the white outline on Street View cars in the Philippines or the tray of a ute on Christmas Island. Vietnamese scenes may include glimpses of a motorbike. Sri Lankan script has 'C'-like characters, while Singapore sports pale green street signs. Find Laos's curved letters differing from Thai's straight letters. Bollards, license plates, and utility poles also hold clues—Thai poles with vertical holes, Indonesian black-divided plates, and Laos's yellow plates. Details lead to destinations!", 'middle_east': "In the Middle East, identifying countries can rely on unique features. For Israel, yellow license plates with a blue stripe are key. The region's languages offer clues: Hebrew signifies Israel, while Arabic points to many Middle Eastern nations. Flat landscapes suggest the Netherlands, unlike the varied terrains of Luxembourg and Israel. Tunisian plates are distinctive, being narrow, black, and long. Turkish landmarks might include distinct guardrails and bollards. Remember, car and landscape details coupled with language can narrow down your guess.", 'rest_of_asia': "In the diverse 'Rest of Asia,' look for unique identifiers: Japan flaunts yellow license plates and yellow-and-black striped poles with low Street View camera angles. Korean writing includes circles and blocky characters. Kyrgyzstan presents cars with visible bars beneath and distinctive black/white side mirrors. Taiwan is known for its utility poles with lower sections covered in black and yellow stripes. Chinese characters are complex with numerous strokes. Spotting these will lead to accurate geolocation in the region.", 'oceania': "In Oceania, geographical features and man-made objects are key to identifying countries. Tutuila in American Samoa showcases a Trekker view with a person holding the camera. New Zealand stands out with unique red 'GIVE WAY' signs, silver utility pole wrappings, and red-numbered highway shields. In Tasmania, spot olive metal pole wrappings. Western Australia is notable for yellow sign poles, while flat landscapes dominate much of Australia, with hills indicating Tasmania or Victoria. The tropical Northern Mariana Islands and Guam have right-hand driving, unlike many islands in the region. American Samoa features blue license plates and double yellow road lines, while Northern Territory plates in Australia may hint a reddish hue. Eucalyptus trees are a telltale sign of Australia. Use these details to narrow down your location within the diverse Oceania region.", 'africa': "When playing Geoguessr in Africa, pay close attention to soil color, with Uganda and Kenya often having red soil. Look for specific road markings like yellow side lines and white centre lines common in South Africa, Botswana, Eswatini, and Lesotho. Recognize Botswana with its unique 'A' and 'B' road designations and striped sign poles. Lesotho's landscape is hilly and tree-scarce unlike green, tree-covered Eswatini. Rwanda stands out with high-quality roads, English/Kinyarwanda signs, and distinct street naming conventions in Kigali. The presence of certain vehicles, from the white Street View car in southern Africa to Kenya's snorkel-equipped Google car, can be major hints. Also, watch out for license plate colors like blue in Senegal or the combination of yellow and green in Eswatini. Wall enclosures are notably prevalent around properties in Rwanda, adding another clue for identification.", 'north_america': "In North America, distinguishing countries can be done by focusing on unique features. Bermuda is identified by a particular black truck or blurred car, unique white roofs blending with the sky, brightly colored houses with white windows, and single, yellow center lines with left-side driving. The USA stands out with 'SPEED LIMIT' road signs and metal pole supports, while Canada has 'MAXIMUM' speed signs, wooden pole supports, black and yellow checkerboard signs, and bilingual signage in New Brunswick. Vehicles without a front license plate generally point towards the southeastern US.", 'latin_america': "Latin America is packed with unique clues. Brazil's transparent satellite dishes, Mexico City's pink taxis with 'CDMX', and Chile's uniform road lines help pinpoint those countries. Peru has Tuktuks, and Puerto Rico lacks front plates on cars. Look for 'BR-' on Brazilian highways, ghostly car fronts in Argentina and Uruguay, and Clasificados Online signs in Puerto Rico. Ecuador features short car antennas, while Colombia sports many yellow plates. Dominican Republic has distinctive green street signs, and Chile's Street View cars have a white rear. These signs and symbols are key to unraveling the puzzle of Latin American locations in Geoguessr."}


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
