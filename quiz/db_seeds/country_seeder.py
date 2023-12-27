from quiz.models import Country, Region
from quiz.helpers import convert_string_to_snakecase

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

OPENAI_CONTENT = {'western_europe': 'Recognizing Western Europe in Geoguessr involves noting distinct details such as driving on the left in Malta, U.K., and Ireland; distinctive bollard details in Spain, Austria, and Germany; road line colors in Ireland and Greece; language cues on signs in Italy, Malta, Spain, and the Netherlands; region-specific license plate features in Switzerland, Belgium, the Netherlands, Malta, and Andorra; geological clues like the mountains in Switzerland, and design elements like the building materials in Andorra and blue tinge of the Street View car in Germany. Keep an eye out for signs in both local and familiar languages, the specific shapes of bollards, utility poles, and guardrails, license plates, the presence or absence of a blue European stripe, and regional road markings for a better guess.', 'eastern_europe': "Recognizing Eastern European locations in Geoguessr relies on subtle yet distinctive visual clues. Romania is recognizable by concrete utility poles with distinctive holes and often a yellow mark. You'll know you're in Ukraine by white-painted utility pole bases and signs in blue with Cyrillic script. Slovakian directional signs have small white arrows, contrasting with Czech signs' large arrows. Language plays a key role too; unique characters like š and ƫ pinpoint Romanian, while multiple occurrences of z and i suggest Croatian. Steering wheel position can hint at Eastern Russia, and Montenegro features visible rifts in the sky when looking upward. Each country has particularities, such as Montenegro's Cyrillic letters С́ and З́, Polish signs with one horizontal line, Russian elongated white license plates, and Hungarian signs with 'UTCA'. Attention to these details, including bollards, road markers, and sign colors, significantly boosts your chances of a correct Geoguessr guess.", 'baltics': "In the Baltics, unique road signs and language characteristics can hint at your location. Latvia's warning signs have thick red borders, while Lithuania's more slender borders include a white outer line; Estonia has no white border. Latvian bollards feature white rectangles on a narrow plank, while Lithuanian bollards display white or orange on a faux-wood design. Estonia's cylindrical bollards contrast with the typical narrow shape found in neighbors. Kilometer markers vary greatly – Latvia's run parallel to the road, Lithuania's feature an arrow shape, and Estonia's sit at right angles. Utility poles are also telling; Latvian 'pine cones' and Estonia's crucifix-style hint at the country. Reflectors can be a tell-tale sign too: Lithuania's guardrails harbor orange reflectors, Latvia's are red and white, and Estonia doesn’t have any. The Latvian language is dotted with horizontal lines over vowels, while Lithuanian has unique letters like ė and combinations like š, ž, č. Estonia's language stands out with letter Ö and a Finnish resemblance, marked by abundant double letters.", 'nordics': "When exploring the Nordics in Geoguessr, pay close attention to languages and signage details. For example, distinctive bollard designs can set Finland apart, while Norway is identifiable by '...vei' or '...veien' on street signs and yellow directional signs. Denmark has unique license plates for commercial vehicles and street names with '...vej' and '...gade'. Swedish signs often feature dashed white lines with gaps longer than the dashes, and its language includes the letters ä, ö, and å. Finnish signs are notable for their blue or green colors and abundance of double letters in the language. Iceland's stark landscapes with little to no trees, along with yellow and black directional signs, are telltale signs. Pay attention to the presence of Swedish and Sami languages in the north of Norway and Swedish and Finnish on signs in certain parts of Finland. Remember, subtle road markings and the Street View car's appearance can also be key clues to your location in the Nordics.", 'south_southeast_asia': "Recognizing locations in Geoguessr within South and South-East Asia hinges on closely observing details such as license plates, street signs, utility poles, and Google Street View vehicle markers. For instance, red plates point to Bhutan, while distinct black rectangles on poles suggest Malaysia's mainland. Language scripts are also clues; hooks in characters indicate Cambodia's Khmer language, while circles at character ends are typical of Thai. Hindi features unique script forms resembling inverted lowercase 'h's and backward capital 'F's, whereas Sinhala from Sri Lanka has 'C'-shaped letters. Additionally, look for the specific Street View markers: a white outline of the car in the Philippines, a silver pick-up tray in Christmas Island, and a helmet in Vietnam's bike-recorded views. Bollards also have region-specific designs, such as match-like in Cambodia and striped obelisks in Thailand. Singapore's street signs, Laos's curved scripts, and Malaysia's bicolored bollards further assist in identifying locations.", 'middle_east': 'In the Middle East, recognizing locations involves identifying language and vehicle details. Hebrew indicates Israel, where vehicles have distinctive yellow license plates with a blue stripe. Arabic suggests a broader range of countries, while specific car models or appearances can point to countries like Tunisia, with its unique long black license plates, or Qatar, evidenced by a commonly blurred white car. Also, look out for infrastructure elements such as B-profile guardrails and bollards, which, though also found in parts of Europe, are markers for Turkey in this region.', 'rest_of_asia': "Recognizing locations in Geoguessr's 'Rest of Asia' region leans heavily on observation of language, vehicles, and utility poles. For instance, yellow license plates are a marker for Japan, while Korean uniquely incorporates circles in its script. Look beneath vehicles too; visible car bars hint at Kyrgyzstan or Mongolia, with the latter sometimes showing 'camping equipment.' Utility pole clues abound; Taiwan features distinctive cylindrical poles striped in black and yellow, a pattern also seen in South Korea. Japanese poles can have similar markings but differ in shape and use of space on the pole. Additionally, bollards and a lower Street View camera angle could point to Japan, while a red stripe on a car plate suggests Kyrgyzstan. Lastly, deciphering the complexity of characters on signs can help distinguish between Chinese, Japanese, and Korean languages.", 'oceania': "In Oceania, Geoguessr players can deduce locations through distinctive features. Look for utilities, such as silver-wrapped poles in New Zealand or olive in Tasmania, and specific pole types like Stobie in South Australia. Road signage differs with New Zealand displaying red 'GIVE WAY' signs and triangle markings, Australia typically uses black. Australian landscapes are flat except in Tasmania or Victoria; yellow plates indicate New South Wales. Notice local fauna, like Eucalyptus trees in Australia. American Samoa and Guam vehicles drive on the right with distinct license plates, and American Samoa's blue plates are unique. Northern Territories have reddish plates; Western Australia has license plates with blue bands. New Zealand's bollards and Australia's bollards differ in design. Signs in Guam confirm US territory, while the Northern Mariana Islands feature tropical landscapes and palm trees.", 'africa': "In African Geoguessr matchups, landscape and road features are key indicators. Uganda showcases distinctive red soil and a visible Street View car, while Kenya has unique truck sightings beneath the camera. South Africa, Botswana, Eswatini, and Lesotho share yellow side lines and white centre road lines, with South African signs being green with yellow numbering. Botswana's signs and poles have specific designs, and Lesotho's lush, tree-scarce hills stand out. Rwanda boasts high-quality roads with faded yellow and white lines, distinctive black trucks, and uniquely coded street signs. Senegal is identifiable by blue license plates and specific Generation 3 Google Car features. In South Africa, the Gen 2 camera's circular blur is often seen, and visibility of the white Street View car extends to its southern neighbors. Driving on the right distinguishes Rwanda from left-driving neighbors like Kenya and Uganda, while high property walls are common in Kigali. License plates in Ghana, Kenya, Rwanda, and Uganda are predominantly yellow, and vehicles often have visible auxiliary equipment, providing further clues.", 'north_america': 'Spotting locations in North America on Geoguessr can be simplified if you look out for distinct cues. In the USA, "SPEED LIMIT" signs and metal poles are your giveaway, whereas Canada\'s "MAXIMUM" speed signs, checkerboard signs, dual-language signage in New Brunswick, and wooden poles are key indicators. Bermuda stands out with unique white-roofed, brightly colored houses, a distinctive black Street View car, and single, yellow center lines indicating left-side driving. Keep these visual clues in mind to pinpoint your virtual whereabouts in North America.', 'latin_america': "Recognizing locations in Geoguessr within Latin America involves paying attention to unique local cues. Brazil's transparent satellite dishes, regional highway labels, and black-painted road signs can confirm your placement in the country. In Mexico, you can identify your location by spotting pink taxis in Mexico City, octagonal utility poles, cigarette-shaped bollards, large black water tanks, circular electricity counters, and unique signs indicating distance to Guatemala City. Peru uniquely features Tuktuks, cigarette-shaped bollards lacking stripes, and distinct three-armed poles. Chile sets itself apart with uniform road line colors, while Argentina and Uruguay show ghostly black Street View car fronts. Ecuador's short antenna under cars and various bollard shapes, Colombia's yellow plates, and the Dominican Republic's green street signs further aid in location identification. In Panama, look for a unique antenna on the Street View car and note that cars often lack front license plates, a feature common in Puerto Rico as well. Lastly, recognizing the side of the road traffic moves on helps differentiate the US Virgin Islands, where driving is on the left."}


def update_regions():
    # Create Regions
    for input_region in INPUT_REGIONS:
        region_name = input_region[0]
        region_sort_order = input_region[1]
        region_db = Region.objects.filter(name=region_name).first()
        if region_db:
            region_db.slug = convert_string_to_snakecase(region_name)
            region_db.description = OPENAI_CONTENT[region_db.slug]
            region_db.sort_order = region_sort_order
            region_db.save()
        else:
            Region.objects.create(
                name=region_name,
                slug=convert_string_to_snakecase(region_name),
                description=OPENAI_CONTENT[convert_string_to_snakecase(region_name)],
                sort_order=region_sort_order
            )
        log.info(f"Region {region_name} updated")
    
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
