import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region, Category


CATEGORY_CHOICES = [
    ('coverage', 'Coverage'), 
    ('driving_direction', 'Driving direction'), 
    ('google_car', 'Google Car'), 
    ('language', 'Language'), 
    ('license_plate', 'License Plate'), 
    ('bollards', 'Bollards'), 
    ('street_markings', 'Street Markings'), 
    ('street_name', 'Street Name'), 
    ('street_sign', 'Street Sign'), 
    ('poles', 'Poles'), 
    ('other', 'Other'), 
    ('cars', 'Cars'), 
    ('buildings', 'Buildings'), 
    ('flora', 'Flora'),
    ('guardrails', 'Guardrails'),
]

OPENAI_CONTENT = {'coverage': "When playing Geoguessr, identifying locations can be made easier by observing the quirks of Street View coverage. In Costa Rica, you're confined to footpaths, in Uganda, you'll find red soil typical of the region around Kampala, and in Kenya. The gravel roads often signal Finland within Nordic setups. Both Albania and Montenegro share the unique feature of sky rifts when looking upwards. Nigeria's older Street View often features a white police car, while India's unmistakable low-quality, 'foggy' footage is a dead giveaway due to unofficial camera equipment. These telltale signs are your breadcrumbs to pinpointing the right location.", 'driving_direction': "Recognizing driving direction as a meta can significantly narrow down the geolocation in Geoguessr. When you're dropped into a location, note if vehicles are driving on the left; this is common in Bermuda, US Virgin Islands, Malta, and surprisingly in some parts of Eastern Russia. Malta's Mediterranean aesthetic sets it apart from other left-driving European countries, while Eastern Russia's right-side steering wheels are an oddity to look for. Conversely, the right-driving Northern Mariana Islands, Rwanda, and American Samoa, which is notable for its double yellow lines and tropical vibes, contrast with neighbors who favor the left. Similarly, cars in Cambodia, Philippines, Laos, and Vietnam keep to the right, which makes them stand out in Southeast Asia. Always consider the landscape and road markings in combination with the driving side to best deduce your virtual whereabouts.", 'google_car': "Recognizing the unique characteristics of Google Street View cars can be crucial in Geoguessr to identify your location. For example, in Kenya, look for a snorkel on the car, while in Senegal, a white truck represents Generation 4 coverage. The Faroe Islands feature jagged, treeless landscapes and grey roof racks, whereas in Ghana, look for a roof rack with distinctive tape and a red rectangle on the car's hood. Chile is distinguishable by the white rear of the car. Uganda and Guatemala show white car edges and black mirrors; Sri Lanka has tricolor stripes, and the US Virgin Islands, Bermuda, and other Pacific islands may display parts of a ute (pick-up truck). Argentina's car appears ghostly black at the front, Vietnam's coverage comes from a motorbike, Ukraine touts a red car with a long antenna, and Tunisia is associated with a dark green Mazda escort. In Germany, you'll see a blue tinge of the newer Street View car, while in Iceland, an aerial is typically visible. These nuances like antennas, car wrappers, and associated vehicles help in pinpointing the location you're virtually dropped into.", 'language': "Recognizing languages in GeoGuessr can hugely impact pinpointing your location. For instance, distinct Slovak letters like Ľ and Ĺ differ from Czech's Ř, Ě, and Ů. Hebrew's character set can signal Israel, while unique Korean circles suggest South Korea. Spotting Sinhala characters shaped like 'C's indicates Sri Lanka, whereas Hindi's upside-down 'h's and Bengali's horizontal lines point to India and Bangladesh respectively. Arabic's calligraphic style spans the Middle East and North Africa, while Mandarin Chinese's complex strokes are key identifiers for China, Taiwan, Hong Kong, and Macau. Khmer's right-pointing hooks are Cambodian markers, just as Thai's small circles differentiate it from Lao's curved letters. Dutch features double vowels and 'ij', Italian ends in vowels frequently, and Icelandic boasts unmistakable characters like Þ and ð. Nordic languages share traits like 'ä' and 'ö', but Finnish's double letters and Estonian's unique Õ set them apart. Spot German with its umlauts and Swiss German's 'ss' instead of 'ß'. Recognizing Croatian's ž, š, and ć, and Polish's 'ł', or Latvian's horizontal line vowels like ā, could lead to those respective countries. Cyrillic scripts in Eastern Europe differ subtly; Macedonian's 'Ѓ' and 'Ќ' or Ukrainian's ґ and і are distinctive, while Serbian flips between Cyrillic and Latin alphabets. These typographic signatures are invaluable for GeoGuessr players to narrow down guesses to specific regions or countries.", 'license_plate': "When trying to determine the location in Geoguessr based on license plates, pay attention to colors, stripes, and shapes. For instance, many southeastern US states may have cars missing a front plate, while in Malaysian and Indonesian plates, the division of white text blocks is key. Color is a strong identifier: yellow plates can hint towards Colombia, the Philippines, or Japan, among others. European countries often have standard features with regional specifics, like the blue stripes of Italy or Portugal's yellow and blue combination. Andorra and Switzerland have distinct deviations from the typical European style. In Australia, state variations like New South Wales' occasional yellow plates or Western Australia's subtle blue strip may give clues. Yellow plates in commercial or public transport vehicles are common in places like Norway, Hungary, and Ukraine. Personalize your look for smaller details such as specific color tinges, unique shapes like Hong Kong's nearly square plates, or special markings, such as the black triangle on Victoria's plates. Understanding these nuances greatly improves the chances of pinpointing the right location.", 'bollards': "Identifying locations in Geoguessr through bollards means paying attention to their shapes, colors, and patterns. In Europe, you'll find unique styles like Serbian bollards with off-center red rectangles, Croatian bollards with red in front and white at the back, and the ubiquitous red rectangles of Ukraine's worn bollards. Poland's bollards stand out with red diagonal stripes. In contrast, Albanian and Finnish bollards have distinctive shapes—the former with vertical and diagonal red on black and the latter with a cylindrical appearance. Asia's bollards differ greatly; for example, Japan's bollards are notably distinct, Cambodia's resemble fat matches, and Thai markers include specific road information. Meanwhile, Austrian bollards have dark reflectors with 'hats,' a feature exclusive to the country. South American bollards like Peru's cigarette-like ones and Ecuador's various shapes with red stripes can be contrasting cues. Always look for these subtle yet telling details to pinpoint your virtual location.", 'street_markings': "When playing Geoguessr, road markings can provide crucial hints about your location. Chile and Argentina both have all-white road lines, but Chile uniquely features all-yellow lines. Denmark's short-dashed edge markings, Russia's blue kilometer markers, and Guatemala's signs indicating distance from Guatemala City are regional specificities. Irish roads with yellow, dashed edge lines contrast the U.K., while French long white dashes are distinctive in Europe. Norway's yellow center with long white side dashes and Sweden's disproportionate side dashes provide Scandinavian indicators. Spain's guardrails with yellow-orange reflectors and Corsica's shorter dashes amidst Mediterranean scenery are tell-tale signs. Icelandic roads with grass up to the dark pavement, Finnish lines with dual yellow centers, and Greece's double white central lines are national identifiers. Rwanda's typically faded yellow and white lines, Malaysia's perpendicular thick yellow markings and its unique black-and-white features, Qatar's sharp black-and-white curbs, Senegal's faded white dashes, and Argentina's white dashes with yellow lines contribute to the portrait of respective regions. Lastly, Uruguay's unique white dashes between yellow lines, Poland's common double middle lines, and Czechia's solid outer lines devoid of a center line help distinguish these from neighboring countries.", 'street_name': "Recognizing street names can significantly narrow down your location in Geoguessr. If you spot 'CALLE,' you're likely in a Spanish-speaking country. 'Rue' points towards French-speaking regions, while 'VIA' is a giveaway for Italy. Dutch street names often end in 'weg' or 'straat,' and Scandinavian suffixes like 'vei' (Norway), 'vej/gade' (Denmark), or 'gatan/vägen' (Sweden) indicate you're in Northern Europe. In Eastern Europe, 'utca' signals Hungary, 'Ulica' Croatia, and 'улица' or 'вулиця' point to Bulgaria and Ukraine respectively. The structure and classification of road signs, such as 'BR-XXX' in Brazil or the unique 'A-Y' naming convention in Chile, can lead to precise country-level identification. Always look out for unique local features like blue signs in Vienna or specific city indicators such as 'KG' in Kigali, Rwanda, or the curved-top signs in Ankara, Turkey.", 'street_sign': "If you're trying to identify street signs in Geoguessr, here's what you need to know: Singapore's pale green signs and the distinctive fonts of Spain are key indicators. Look for language and color patterns, like the bilingual nature of Canadian and Irish signs or the unique styles found in Nordic countries, such as Norway's yellow directional signs. Australia's yellow or silver poles, New Zealand's red 'GIVE WAY' signs, and South East Asia's typical yellow diamond-shaped warning signs can point you to the right region. Latin America has varied sign styles, with country-specific features like the striped poles in Uruguay. The Middle East often includes both local script and English, aiding in quicker identification. Strategic use of alphabet, color, and additional language can be telltale signs for countries like Russia, Ukraine, and Bulgaria. For deciphering European signs, pay attention to background and border colors, such as the green or blue directional signs in Hungary and the clear border distinctions between Czech and Slovak signs.", 'poles': "Recognizing the right utility poles in Geoguessr can be a game-changer. Look for unique features, such as the 'holey poles' with large vertical holes in Hungary and Romania, or the octagonal shapes and black and yellow stripes that indicate Mexico or South Korea. In Eastern Europe, you'll find variations like the 'Eiffel Tower' poles in Bulgaria and pine cone adornments in Baltic nations. Painted bases such as the white in Ukraine or the metal wrappings in Tasmania and New Zealand also provide strong regional clues. Remember, these details vary widely and can point you to the correct continent or even the exact country, like the crucifix poles in the Philippines or the specific regional plates on Japanese poles. Keep your eyes peeled for these subtle yet distinctive signs!", 'other': "Mastering the art of location identification in Geoguessr hinges on recognizing subtle cues. From the blue rectangle on Taiwanese poles to the red and white Bangladeshi fences, these metas are critical. Flags painted on Ukrainian objects, Argentinian tree-lined streets, and PT company signs in Indonesia all provide vital, country-specific hints. Pay attention to unique regional traits like Jeju's rock walls in South Korea, Peruvian electricity counters, Croatian and Hungarian fire hydrants, and Malaysian Sdn Bhd company signage. Local nuances like internet suffixes (.rs for Serbia), satellite dish angles in Indonesia, or even the presence of certain animals, like tortoises in the Galapagos and albatross in Midway Atoll, can significantly pinpoint your geolocation. Additionally, phone area codes in Brazil or rudimentary fences in rural Colombia can narrow down the search effectively.", 'cars': "Recognizing cars in Geoguessr can offer location clues; Tuktuks hint at Peru, Mexico City features distinctive pink taxis labeled 'CDMX,' and green and red taxis signal Hong Kong. In the Philippines, lookout for colorful mini-buses and rickshaws, while Bangladesh is known for traditional bike-front rickshaws and left-side driving. Japanese cars tend to be boxy. Colombian taxis and trucks often display city names on side plates or roofs, with 'Bogota' being a common sighting. These vehicle features can be key indicators of your virtual whereabouts.", 'buildings': "Recognizing buildings in Geoguessr can significantly help pinpoint your location. For example, Andorran buildings with distinct gray stone construction or Bermuda's bright-colored houses with striking white roofs are characteristic of those regions. Similarly, Mexico's circular electricity counters and black water tanks on houses are strong indicators of their location. Colorful Greenlandic houses; Swiss wooden houses with frequent window shutters; Brazil's transparent satellite dishes; Rwanda's high-walled properties; Malaysia's vertically columned houses; UAE's skyline with potential views of tall skyscrapers, particularly in Dubai; Bhutan's detailed architecture with flat extended roofs; Cambodian stilt homes; Chile’s unique bus stop shelters, even in rural areas; and Curaçao's vividly painted homes are all architectural features you can rely on to narrow down your guesses to those specific areas.", 'flora': "Recognizing locations in Geoguessr by flora involves noting unique vegetation and landscape features specific to regions. In Australia, look for Eucalyptus trees and generally flat landscapes, with Tasmania and Victoria featuring rolling hills. Luxembourg's gentle slopes and green grass fields contrast the mountainous terrain in Norway, which is heavily vegetated compared to Iceland's sparse grasslands peppered with volcanoes and glaciers. Switzerland boasts tall mountains and wooden houses with specific roofing, while Ukraine's trees often have white-painted trunks. Malta's low-lying rock walls and limited vegetation, Eswatini's green, hilly landscape with trees, and Lesotho's treeless hills help distinguish these locations. Bhutan's towering, wooded mountains; Madagascar's coastal areas; Japan's Hokkaido with unique vegetation; and the tropical environments of Sri Lanka, Thailand, and Ecuador, characterized by palm trees and lush greenery, are indicative of their respective regions. Noting these climate-dependent features will sharpen your geographic deduction skills on Geoguessr.", 'guardrails': "If you're playing Geoguessr and notice guardrails in your location, pay attention to their features. Lithuania's guardrails with orange reflectors are distinctive, setting them apart from Latvia's red and white reflectors and Estonia's lack of reflectors, which can be crucial clues for the Baltic region. Ecuador stands out with its double-stacked guardrails, a unique design that could quickly lead you to pinpoint South America. In Central Europe, both Czechia and Slovakia use type B guardrails, wider in the middle, which can be tricky but knowing both countries share this feature may require you to look for additional context to differentiate them."}


def update_categories():
    # Create Categories
    for input_category in CATEGORY_CHOICES:
        category_db = Category.objects.filter(slug=input_category[0]).first()
        if category_db:
            category_db.name = input_category[1]
            category_db.description = OPENAI_CONTENT[input_category[0]]
            category_db.save()
        else:
            Category.objects.create(
                name=input_category[1],
                slug=input_category[0],
                description=OPENAI_CONTENT[input_category[0]]
            )
        log.info(f"Category {input_category[1]} updated")
    
    # Delete Categories
    db_categories = Category.objects.all()
    input_category_slugs = [input_category[0] for input_category in CATEGORY_CHOICES]
    for db_category in db_categories:
        if db_category.slug not in input_category_slugs:
            if db_category.quiz:
                db_category.quiz.delete()
            db_category.delete()
            log.info(f"Category {db_category.name} deleted")


def update_quizzes():    
    # Category Quizzes
    categories = Category.objects.all()
    for category in categories:
        # Name
        quiz_name = category.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if quiz_db:
            quiz_db.category = category
        else:
            quiz_db = Quiz.objects.create(name=quiz_name, category=category)    
        
        # Add Quiz FK to Category
        category.quiz = quiz_db
        category.save()
        
        log.info(f"Quiz {quiz_name} updated")
    

    # Region Quizzes
    regions = Region.objects.all()
    for region in regions:
        # Name
        quiz_name = region.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
        
        # Set all countries in region
        countries = Country.objects.filter(region=region)
        quiz_db.countries.set(countries)
        
        # Add Quiz FK to Region
        region.quiz = quiz_db
        region.save()

        log.info(f"Quiz {quiz_name} updated")
    
    
    # Country Quizzes
    countries = Country.objects.all()
    for country in countries:
        # Name
        quiz_name = country.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
        
        # Set country
        quiz_db.countries.set([country,])
        
        # Add Quiz FK to Country
        country.quiz = quiz_db
        country.save()

        log.info(f"Quiz {quiz_name} updated")
    
    
    # Create 'Random' quiz for all facts
    random_quiz_name = Quiz.RANDOM_QUIZ_NAME
    try:
        quiz_db = Quiz.objects.get(name=random_quiz_name)
    except Quiz.DoesNotExist:
        quiz_db = Quiz.objects.create(name=random_quiz_name)
    log.info(f"Quiz {random_quiz_name} updated")
    
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        
        # Delete quiz if no facts
        quiz = Quiz.objects.get(uuid=quiz.uuid)
        if quiz.num_facts == 0:
            quiz.delete()
            log.info(f"Quiz {quiz.name} deleted")
    
    Quiz.objects.filter(name="Geometas - All Random").delete()
        