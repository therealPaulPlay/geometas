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

OPENAI_CONTENT = {'coverage': "Street View coverage tells a lot about location. Limited coverage to footpaths, like in Costa Rica, means you can't leave the path. Nordic gravel roads might point to Finland. A low camera angle is unique to Switzerland and Japan, making you feel closer to the ground. Watch for a rift in the sky in Montenegro and Albania. In Uganda, red soil is common, but it can also be found in Kenya, mostly around Kampala.", 'driving_direction': 'Driving direction is a key clue in GeoGuessr. Countries like the UK, Ireland, and Malta drive on the left in Europe, which is rare. Island nations often have their own patterns; Bermuda and the US Virgin Islands also drive on the left. However, American Samoa and the Northern Mariana Islands are exceptions, with right-hand traffic. Look for steering wheel placement, particularly in places like Eastern Russia, and road markings, as these are indicative of the local driving habits and can significantly narrow down your guessing options.', 'google_car': 'The Google Car meta can be a key factor for Geoguessr users to identify locations. Each country may have peculiar features on the Street View car, like unique antennas, car colors, or equipment. Some countries show a white car or truck, some have visible roof racks, while others have snorkels or aerials. The absence of certain elements, such as aerials in specific Eastern European countries, can also be a telling sign. Look for distinct characteristics like snorkels in Kenya or motorbike imagery in Vietnam to narrow down your guesses.', 'language': "Recognizing countries in GeoGuessr by language involves looking for unique alphabets and specific letters. In areas using the Latin alphabet, diacritics are key indicators—like Slovakia's Ľ, or Romania's ș. Cyrillic and unique characters point towards Slavic nations. Asian scripts vary greatly: Sinhala's 'C-like' characters for Sri Lanka, Hindi's backward 'h's for India, and Korean's distinct circles. For Hebrew and Arabic, look for right-to-left script. Nordic languages have characteristic vowels such as 'ä' and 'ö'. Compare subtle differences in character complexity to identify Chinese, Japanese, and Korean writing. Always pay attention to these specific linguistic nuances—they're your best clue.", 'license_plate': 'License plates can offer crucial clues in Geoguessr. Often, colors, stripes, and symbols help pinpoint a location. Yellow plates may suggest places like the Netherlands or parts of Africa. In Europe, blue stripes are common, except for countries like Switzerland without them. The US varies widely; for example, states in the south-east may lack front plates. Latin American plates vary, with some countries like Argentina having distinctive features. Recognizing these details, like plate size or special stripes, improves your location guessing game.', 'bollards': "Bollards are key indicators of location when playing Geoguessr. They often have unique shapes, colors, and reflective patterns. Typically, you can identify a country by its bollard style. Serbian bollards have a red rectangle to one side, while Czech and Slovakian ones feature unique fluorescent orange stripes. Ukrainian bollards have a wider red rectangle and are often run-down. In contrast, Polish bollards feature a distinctive red diagonal stripe. Look for narrow support poles to distinguish Russian bollards from Ukrainian ones, and remember that Finnish bollards are unique in their cylindrical shape within the Nordics. Austrian bollards are easily spotted by their dark reflectors, and South Africa replaces bollards with narrow red and white signs. Each country's bollards have distinguishing features that can provide crucial clues to your virtual location.", 'street_markings': 'Street markings are crucial for pinpointing locations in Geoguessr. Look out for the color and pattern of road lines. While yellow lines may indicate countries like South Africa, white-lined roads are common in Europe. Distinctive dash lengths or dual-color lines can narrow down your options. Short dashes often signify Denmark, while long white dashes hint at France. Guardrail reflectors also offer clues; yellow-orange ones could lead you to Spain. Always pay attention to the unique combination of markings and the overall road quality to best identify your location.', 'street_name': "Recognizing the country in Geoguessr isn't just about landscapes; street names are big clues. Words like 'CALLE', 'rue', or 'VIA' point to language and hence region. The design of street signs—color, shape, the presence of a city name—also helps. For example, blue or green signs might suggest specific countries. Always note suffixes ('...weg', '...straat', '...vei'), as they can be unique language indicators. Differentiating regions is about combining language and sign design with your surroundings.", 'street_sign': "Street signs are crucial clues in Geoguessr. Specific colors, text, and shapes can pinpoint your virtual location. Look for color schemes (green in Singapore, blue in Ireland), text language (bilingual in Canada), and shape (diamond in Ireland). Pedestrian crossing signs vary in dash count. In the USA, 'SPEED LIMIT' is written, while Canada uses 'MAXIMUM'. Unique elements like checkerboard patterns in Canada, bilingual signs in New Brunswick, and distinctive yellow signs in Iceland help narrow down the country. Remember, regional variations within countries and similar-looking signs across borders can be tricky.", 'poles': "Looking closely at utility poles can be a game-changer in pinpointing your location. Unique identifiers include pole shapes (octagonal, cruciform, square), surface patterns (stripes, indents, 'pine cone' protrusions), and specific markings (yellow/black stripes, rectangles with lettering, color bands). Also, notice the pole bases and hole patterns—they vary significantly by country. Take note of metal or color wrappings at the base, as they can be exclusive to certain areas. Poles are like signatures—no two countries' poles are exactly alike, though some share similarities.", 'other': "Recognizing a country in Geoguessr often comes down to unique visual cues, such as local architecture, street signs, or even internet domains. Pay close attention to things like the style of electricity meters, the design of fire hydrants, advertisement signs, and even what follows the country's street view car. Each country has its quirks, like Serbia's '.rs' domain or the distinct landscape in Botswana. Spotting specific wildlife or landmarks can also be a giveaway, as in Midway Atoll’s albatrosses or Christmas Island’s red crabs.", 'cars': "Cars can be a great clue for pinpointing locations. Tuktuks are a telltale sign of Peru in Latin America, as no other countries in that region have them. In Mexico City, look out for pink taxis, unique to the area, with 'CDMX' marking their connection to 'Ciudad de México'. Recognizing vehicle types and local taxi colors can narrow down your location significantly.", 'buildings': "Building styles are key in Geoguessr to recognize locations. Look for unique features: Andorra has affluent stone buildings, Bermuda boasts semi-faded colorful houses with stark white roofs, Mexico has visible circular electricity counters and black water tanks, Nordic houses are often reddish-brown, and Swiss buildings typically have window shutters and are wooden. Rural Baltic homes may have eternit roofs, Brazil's satellite dishes are transparent, and high walls around properties are a clue for Rwanda.", 'flora': "Flora and landscape are crucial clues in Geoguessr. Recognizing the tree types and terrain can often pinpoint a location. Look for unusual trees like Australia's Eucalyptus, which are tall with distinct white bark. Terrain also varies; gentle slopes suggest Luxembourg, while hilly or mountainous landscapes hint at Norway or Eswatini. Lack of trees in otherwise green, hilly areas could be Lesotho or Ukraine with painted tree trunks. Wooden Swiss houses with slanting roofs amid mountains, or New Zealand's South Island vistas offer other strong regional markers.", 'guardrails': "Guardrails can be a subtle yet distinguishing feature in Geoguessr. Colors of reflectors are often region-specific; for instance, Lithuania's orange versus Latvia's red and white. Guardrail designs vary, from the unique B-profile rails in parts of Central Europe and the Balkans, to the wide central section types in Czechia and Slovakia. Notice these patterns and designs to pinpoint your location."}


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
        