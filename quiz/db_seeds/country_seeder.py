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

OPENAI_CONTENT = {'western_europe': "Recognizing locations in Western Europe on Geoguessr hinges on identifying unique road features, language cues, and license plates. Distinctive bollard designs signal countries like Spain, Austria, and Italy, with color and patterns setting them apart. Countries like Malta and the UK stand out for driving on the left, while specific road markings like yellow dashed lines can point to Ireland. Text cues are equally vital; different languages use unique alphabets or characters, such as the Greek alphabet or the 'ß' character in German. Additionally, the presence or absence of the blue European strip on license plates can differentiate countries like Switzerland, Andorra, and the Isle of Man. Localized sign words like 'CALLE' or 'Triq' pinpoint Spanish and Maltese streets, respectively. License plate colors and shapes also serve as clues; Belgium's red lettering, the Netherlands' yellow plates, and Switzerland's 'CH' stickers are giveaways. Lastly, regional geography such as the Mediterranean look of Malta, the mountains of Switzerland, or Luxembourg's undulating terrain can be determinative.", 'eastern_europe': 'Recognizing locations in Eastern Europe on Geoguessr hinges on subtle clues like specific characters in local language scripts, distinctive traffic infrastructure, and regional signage norms. In Russia, the placement of steering wheels and blue highway distance markers can guide you, while unique letters signal Czechia (Ř, Ě, Ů) and Slovakia (Ľ, Ô, Ä). Poland stands out with its double middle lines and "holey" utility poles. Serbian bollards have a red feature that\'s offset, and attention to the base color of utility poles can pinpoint Ukraine. Guardrail and bollard styles vary from Croatia\'s narrow blue hydrants to Slovenia\'s kilometer markers, all providing vital hints. Signage, from the color of directional signs to the bolt patterns on Hungarian signs, alongside the presence or absence of a Google car antenna, serve as critical visual cues. Licenses plate styles, language nuances, and even regional internet suffixes enhance the identification process.', 'baltics': "To crack the Baltics in Geoguessr, focus on unique markers: Latvia's thick red-bordered warning signs, distinct 'pine cone' utility poles, parallel blue km markers, and red/white guardrail reflectors set it apart. Lithuania's language features unique letters like ė, š, ž, and č, endings in '...ai' or '...as', and its km markers have a double sign design with orange guardrail reflectors. Estonian similarities with Finnish, unique letters Õ and Ä, right-angle km markers, crucifix-like utility poles, and distinctive cylindrical bollards with a white or yellow rectangle encapsulated by black should point you to the correct Baltic country.", 'nordics': "Mastering the art of location identification in Geoguessr within Nordic countries means getting familiar with a host of region-specific details. Differentiating between these countries relies on noticing nuances in language, unique road signs, and the environment. Danish signs are marked by a distinctive use of red and white, with directional signs following this theme and featuring unique suffixes like '...vej' and '...gade'. Common vehicles have yellow plates, distinct from Norway, where commercial ones sport green plates, and directional signs include a combination of yellow and Sami language in the north. Sweden's road markings and linguistic details like 'ä' and 'ö’ are telltale, as are signs ending with '...gatan' and '...vägen'. The Finnish language is notable for its double letters and bilingual signs in Swedish and Finnish to the southwest, while their road markings are typically white with a yellow centerline. Icelandic landscapes are stark, often displaying flat roads with hills in the distance, and lack the blue stripe on license plates. Spotting colorful Greenlandic houses or the Icelandic letters 'Þ' and 'ð' are definitive clues of your location. Pay attention to these specific attributes to pinpoint your Nordic location on the Geoguessr map with confidence.", 'north_america': "When pinpointing locations in North America on Geoguessr, note region-specific details: Bermuda's unique black Street View vehicle, distinctive bright-colored houses with stark white roofs, and left-side driving with a single yellow center line. In Canada, look for bilingual signposts, especially in New Brunswick, checkerboard black and yellow signs, and wooden or white-painted sign poles, with 'MAXIMUM' on speed signs. The US has 'SPEED LIMIT' signage, metal poles, and in the southeast to some western states, cars may lack a front license plate. These visual cues are key to accurate geolocation.", 'latin_america': "Recognizing Latin American locations in GeoGuessr hinges on observing unique regional features: Colombia is identified by crosses on signs and distinct vehicle plates; Brazil stands out with transparent satellite dishes and red license plates for commercial vehicles; Mexico has pink taxis, octagonal utility poles, and large black water tanks; Chile can be spotted by bus shelters even in rural areas and white road lines; Uruguay's traffic lights are on striped poles, and cars often lack a front plate; Ecuador features unique orange plates and double guardrails; Peru's bollards and signs are distinctive, and their houses have rectangular electricity counters. Less common are details like Curaçao's Dutch languages and the US Virgin Islands' left-driving cars. Each country has its own street sign styles, vehicle characteristics, and road markings which, once familiar, are telltale signs of their respective locations.", 'south_southeast_asia': "In South & South-East Asia, you can navigate Geoguessr by recognizing specific meta details: the crucifix-style wooden utility poles in the Philippines; the prevalence of rickshaws and left-hand driving in Bangladesh; the distinctive angle of satellite dishes in Indonesia; the written Khmer language in Cambodia with small right-pointing hooks; asymmetrical utility poles with 'pine cones' in Laos; Singapore's three-letter highway codes and district-named roads; yellow diamond-shaped warning signs with white outlines in Cambodia, and abbreviation 'Jl.' for streets in Indonesia. Spot elevated Cambodian houses, pinpoint in Malaysia with thick yellow lane lines, and observe unique license plates in Bhutan (red) and India (various colors, with blurriness due to unofficial Street View camera). In Pakistan, expect trekker capture often around temples, and in Vietnam, a motorbike capture. Singapore streets have pale green signs, and Thailand features wooden signposts with black bases. The French-flag-striped Street View car is your clue for Sri Lanka. These localized cues, alongside regional landscapes and architecture, guide your guesses effectively.", 'middle_east': "Recognizing locations in the Middle East on Geoguessr involves looking for specific visual cues and language characteristics. Israeli street signs feature trilingual text and distinct color-coded road categories, while their yellow license plates have a unique blue stripe. Arabic is the dominant language in Palestine, with elongated white license plates that differ from Israel's. In the UAE, you're likely to spot white Street View cars and black and white curbs, with the backdrop of Dubai's towering skyscrapers being a dead giveaway. Turkey's signs include hooked letters 'ş' and 'c,' with red and white road arrows and blue or green directional signs, plus kilometer markers that help identify roads. Qatar showcases bilingual signage and maroon-accented license plates. Tunisia's setting gives off a Middle Eastern ambiance, with French on signs, dark green Toyota Street View followers, and palm tree landscapes with Mediterranean architectural influences. Jordan's blue signs with white lettering and green highway markers, along with black Street View cars, also aid identification. Analyzing these meta traits can significantly improve your location-guessing accuracy in this diverse region.", 'rest_of_asia': 'Recognizing locations in the "Rest of Asia" region in Geoguessr hinges on distinguishing characteristic details from Japan, South Korea, Hong Kong, Chin, Taiwan, Mongolia, and Kyrgyzstan. Japan can be identified by yellow license plates, blue directional signs with white lettering, black and yellow striped poles, and specific utility pole plates that vary by region. South Korea features utility poles with pointed spikes, green highway signs with white lettering, and triangular warning signs with red borders and yellow fill. Taiwan has green directional signs, often with English and Mandarin lettering, and utility poles with black and yellow stripes. Notably, language scripts differ: Japanese characters are simpler with fewer strokes, while Chinese characters are more complex; Korean text incorporates distinct circles. Mongolia has unique Street View car equipment, and Kyrgyzstan\'s license plates have a red stripe. Busily numbered yellow road markers and square-shaped license plates can hint at being in Hong Kong. Each country has specific cues that, when recognized, greatly improve the chances of an accurate Geoguessr guess.', 'oceania': "In Oceania's Geoguessr locales, spotting utility pole colors and types is key—silver in New Zealand, olive in Tasmania, and distinctive Stobie poles in South Australia. Note the signage differences, with white street signs in Australia against New Zealand's blue or green ones, and red on 'GIVE WAY' signs in NZ compared to black in Australia. In American Samoa, car perspectives or the view of a carrier instead of a car point to location, along with blue license plates and driving on the right with double yellow lines. Western Australia stands out with yellow sign poles, and the Northern Territory's red license plate tinge. Palm trees and US-style signs may hint at the Northern Mariana Islands, while Tasmania's olive pole wrappings are unique. Lastly, look for Tasmanian and Victorian 'C' roads and eucalyptus trees as typical Australian markers.", 'africa': "In Africa, identifying locations in Geoguessr can be nuanced with vehicle, soil, and sign indicators. For example, in Nigeria, look for escort vehicles and distinct utility pole markings. Senegal often features faded white road dashes and blue license plates. Uganda's tinges of green and red soil are unique, with visible Street View car equipment. Botswana has unmistakable sign poles with black and yellow stripes, and high-quality, flat landscapes. In Lesotho, expect treeless, green hills. Madagascar offers coastal views and Antananarivo's elevated areas. Kenyan Street View has snorkels on vehicles, a distinct giveaway. High walls and bilingual signs are prominent in Rwanda. South African roads have green signs with yellow lettering, while in Eswatini, the hilly terrain with trees contrasts with Lesotho. Lastly, a tropical, French-speaking environment suggests Reunion. Recognizing these features can greatly aid in pinpointing your location."}


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
