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
    ('street_numbering', 'Street Numbering'), 
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

OPENAI_CONTENT = {'coverage': "Coverage can be a dead giveaway. For instance, Costa Rica's views are captured by trekker, not a car, so you're bound to be on footpaths only. A low Street View camera in Switzerland and Japan creates a 'closer to the ground' illusion. Occasionally, Sri Lanka and Taiwan may also give you this low view. In contrast, Nordic terrain often shows dirt or gravel roads, hinting at Finland. Look up in Montenegro and Albania - a telltale rift in the sky often appears.", 'driving_direction': "Recognizing the driving direction can be a giveaway to the country you're viewing. Countries where cars drive on the left are less common and include nations like the UK, Ireland, Malta, Bermuda and territories like the US Virgin Islands. Look for road markings, such as a single yellow centre line, or other traffic patterns and signs indicative of left-hand traffic to confirm your guess.", 'google_car': 'Recognizing locations in Geoguessr can hinge on spotting unique features of the Google Street View car. Keep an eye out for distinctive traits like snorkels, roof racks, car colors, and antennas. In some regions, the shape or equipment of the Street View vehicle is unique, such as motorbikes or escort vehicles. The color and accessories, like bars and mirrors, can also offer clues. Look for anomalies like blurred sections or distinctive vehicles following the car, and note the overall color scheme or presence of aerials to pinpoint your location.', 'language': "Language metas are keys to unlocking the country in Geoguessr. Each language has unique characters or scripts. For example, specific accent marks, like Ľ, Ô, Ä in Slovak or the presence of Ř, Ě in Czech, pinpoint nations. Sinhala resembles chains of 'C' shapes, distinguishing Sri Lankan locales. Hindi's upside-down 'h's and straight-backed 'F's set it apart, while Arabic scripts flow with lines underneath. Chinese characters have denser strokes compared to Japanese and Korean; note Japanese's simpler curves and Korean’s distinct circles and block shapes. By recognizing these language traits, from the circles in Thai to the hooks in Khmer, Hebrew's fluidity to Dutch double letters, Italian vowels endings, or Nordic languages' dots and rings, players enhance their detective skills in determining the correct country.", 'license_plate': "License plates can be a goldmine of hints in Geoguessr. Keep an eye out for distinctive colors, shapes, and symbols. Certain countries have unique colors like yellow in the Netherlands or black in Malaysia. The presence or absence of a front plate is also telling; many US states only require rear plates. Vertical stripes offer clues; for example, blue stripes are characteristic of European countries but their presence, position, or absence can narrow down the choices. Some countries like Switzerland and Norway have variations for commercial vehicles. Always check for special markings like country codes (e.g. 'CH' for Switzerland), which can be a clear giveaway.", 'bollards': "Bollards can be key to identifying a location. In Geoguessr, focus on their shape, color, stripes, and attached features. For example, Serbian bollards have a red rectangle to one side, but it's centered in Slovenia and Montenegro. Czech and Slovakian ones have unique orange stripes. Look for the broader red rectangle on Ukrainian bollards, while Russian ones have a narrow support pole. Italian bollards have a black diagonal strip with a red rectangle, a rarity in bollard designs. Remember, each country has its distinctive bollard style that can clue you into your virtual whereabouts.", 'street_numbering': "Recognizing street numbering systems can be a powerful clue. Brazil uses 'BR-XXX' for national and 'YY-XXX' for state highways—'YY' being state codes. In Russia, federal highways are marked with M, A, or P/R—the M roads encircle Moscow. Minor roads in France use 'D' followed by a number, usually on a yellow sign. Look for these patterns to identify the country's roads you're viewing. They are unique and vary significantly between countries, hence a good indicator of location.", 'street_markings': 'Street markings are key in Geoguessr to pinpoint your location. Different countries have specific styles for center and edge lines. Look for color distinctions like all white or all yellow lines, or unique patterns such as short dashes on edges or long dashes. Some countries use numbers on markers to indicate distance, a detail to watch for. Note the presence and pattern of dashed lines: do gaps outnumber the dashes or vice versa? Reflectors on guardrails can also be a telltale sign of a region. Always observe the overall road conditions and surrounding landscape, as these enhance your recognition of the specific street markings.', 'street_name': "Street names hold vital clues in Geoguessr. Look for sign suffixes revealing language & region. 'Calle' points to Spanish-speaking regions while 'weg' and 'straat' are Dutch indicators. French 'rue' suggests a French-speaking area. Nordic countries show distinct patterns: Norway with 'vei(en)', Sweden with 'gatan/vägen', Finland with 'katu/ntie', and Denmark with 'vej/gade'. Italy's 'Via', Hungary's 'Utca', and Croatia's 'Ulica' signal their respective languages. Additionally, Austrian 'blue' and Belgian city-labeled signs hint at location. Absorb suffix patterns to pinpoint countries!", 'street_sign': "Street signs are a crucial indicator in Geoguessr to pinpoint your location. Each country has unique features. Look for specific font styles, colors, and language. For example, specific fonts and colors can reveal if you're in Singapore, Spain, or the USA. Bilingual signs can suggest Canada or Ireland. Shape of signs, like diamonds in Ireland, or the yellow and black checkerboard in Canada are telltale signs. Remember the pole types, too. Wooden poles could mean Canada, metal might indicate the USA. These details, along with how warning and direction signs are styled, can narrow down your guesses significantly.", 'poles': "Utility poles help identify locations in Geoguessr. Look for distinctive features like pole shape, presence of holes or indents, and unique markings. Octagonal poles suggest Mexico, while poles with vertical stripes might indicate Japan or South Korea. Recognize Malaysia by black rectangles with white lettering on poles. In Europe, differences in holes and indents can separate Romania, Hungary, Spain, or Poland. The Baltic countries exhibit unique 'pine cone' attachments or crucifix shapes on poles.", 'other': 'Recognizing a country by its unique objects, like electricity meters, signboards, or fire hydrants, is a clever approach. Look for shape, color, and design specific to a region. Red-white signs may indicate Puerto Rico, while distinct hydrants could point to Hungary or Croatia. Always keep an eye out for these subtle yet distinct clues scattered in urban and rural landscapes to pinpoint your location.', 'cars': "For the cars category, unique vehicles like tuktuks in Peru help identify your location. Pink taxis are a giveaway for Mexico City; look for 'CDMX' marking on these taxis or on signs throughout the city. Pay attention to vehicle types, taxi colors, and markings for clues.", 'buildings': "Buildings can offer vital clues in Geoguessr. Look for distinctive architectural features, materials, and colors. Andorra sports gray stone buildings, while semi-faded bright colors with white roofs mark Bermudian homes. Mexican buildings often have circular electricity counters outside and black water tanks sitting above. In the Nordics, expect reddish-brown houses, unlike Greenland's colorful palette. Switzerland’s wooden houses with multiple shutters are telling signs, as are rural Baltic homes with eternit roofs. In Latin America, transparent satellite dishes are distinct to Brazil.", 'flora': "Flora gives vital clues about location. Look for unique vegetation like tall, white-barked eucalyptus in Australia, which stands out. Terrain is also a strong indicator. Luxembourg has undulating terrains with green grass fields, unlike the flat lands of the Netherlands. Norway's landscape is hilly and mountainous, a contrast to the generally flat Nordic countries, while Iceland features grassy landscapes with volcanic and mountainous backdrops. Switzerland is known for its tall mountains and distinctive wooden, multi-storey houses with terracotta roofs.", 'guardrails': 'Guardrails can be a subtle clue in Geoguessr. Look for colored reflectors: orange ones point to Lithuania, red and white to Latvia, none suggest Estonia. A B-profile guardrail with 90-degree angles hints at countries like Croatia, Serbia, Poland, and Denmark, also seen sporadically in Turkey, North Macedonia, Ireland, and Germany. Wide central guardrails are unique to Czechia and Slovakia. Spot these features to narrow down your location guesses in Europe.'}


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
        