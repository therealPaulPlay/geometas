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

OPENAI_CONTENT = {'guardrails': '', 'coverage': "Coverage can be a critical meta in Geoguessr for identifying locations. In some countries like Costa Rica, Street View only covers footpaths, a unique feature that can distinguish it from others. You can't move off the path, which is a significant hint. In Nordic countries, the presence of dirt or gravel roads suggests you may be in Finland, as this is common there. Pay attention to the type of Street View available and the nature of the paths or roads to best determine the country.", 'driving_direction': "The side of the road on which vehicles drive is an important clue in Geoguessr. Fewer countries have left-hand driving compared to right-hand. Bermuda, the U.K., Ireland, and Malta are notable for driving on the left. Spotting a single yellow centre line might hint towards Bermuda. Despite being a US territory, the US Virgin Islands also feature left-side driving, deviating from the mainland's norms. Pay attention to road markings, car positions, and any surrounding signs, which could affirm the driving side.", 'google_car': 'Recognizing the Google Street View car can be key in Geoguessr. Unique features like snorkels, roof racks, and antenna types can hint at specific countries. Look for snorkels in Kenya, a silver truck in Senegal, or distinct car roofs like the grey one in the Faroe Islands. Some cars have distinct colors or patterns; for instance, Sri Lanka’s car has blue, white, and red stripes. In Uganda, white edges and black mirrors are noticeable, while Russia often shows a black car with a long aerial. Pay attention to these small details and car equipment to best gauge your virtual location.', 'language': "Recognizing the language in Geoguessr can guide you to the right country. Unique characters or alphabets offer clues. For example, Ľ or Ř point to Slovakia and Czechia, respectively. Sinhala resembles a series of 'C' shapes, while Hindi has upside-down 'h' characters. Arabic script features seamless lines with curves. Chinese characters are intricate compared to Japanese's simpler strokes and Korea's blocky texts with circles. Look for specific hooks in Khmer, circles in Thai, and complete curves in Lao. Dutch often pairs 'ij', while Italian words mostly end in vowels. Icelandic's Þ and ð are dead giveaways. Nordic languages exhibit telltale dots or circles above certain vowels and double letters, key in distinguishing them from one another.", 'license_plate': "License plate features significantly boost Geoguessr gameplay. Pay attention to color, stripes, and distinctive symbols. Front plate presence varies, with some regions and countries not requiring them. Europe generally sports standard blue vertical stripes, distinguishing some by color, like Belgium's red lettering or Portugal's yellow stripe. Look for unique hues like Japan's and Brazil's yellows or Tunisia's black. South America leans towards yellow, while Africa's Rwanda and Uganda share that trend. No plate on the front? Consider the US, Puerto Rico, or Panama. The presence of a blue stripe often signifies European origin, but specifics like Italy's light blue or Luxembourg's flat terrain narrow it down. Yellow plates could point towards Asian countries like Laos. Each detail is a valuable clue to pinpoint your virtual location.", 'bollards': "Bollards are key indicators for pinpointing locations in Geoguessr. Look for unique colors, shapes, and patterns. Serbian bollards have offset red rectangles. Czech and Slovakian ones flaunt distinct orange stripes. Ukrainian bollards are often worn with wide red rectangles, unlike the neater Russian ones with a support pole. In Turkey, expect thicker rectangles, akin to Australia and the Netherlands. Italy's bollards stand out with a full-length diagonal stripe. Finnish counterparts are cylindrical. Yellow-topped Icelandic bollards, reflective Austrian ones, and distinctively shaped French and Mexican variants all give away their locations. Watch for color variations on the backs of bollards in different countries to make the right guess.", 'street_numbering': "Street numbering can be a quick tip-off to your geolocation. Different countries have unique systems for labeling their roads. Brazil uses 'BR-' for national highways and state abbreviations for regional ones. In Russia, look for prefixes like 'M', 'A', or 'P/R' on road signs, with 'M' roads encircling Moscow. France's minor (departmental) roads carry a 'D' prefix within a yellow rectangle. Spotting these specifics in signs can narrow down your country guess significantly.", 'street_markings': 'Street markings are key clues when identifying a location. Pay attention to the color and pattern of road lines, as certain countries have characteristic styles. Look for the color contrast between the center and side lines, the length and spacing of dashes, and unique markers like distance signs or specific reflectors. These subtle details can be the difference between countries with similar landscapes but different road marking standards.', 'street_name': 'Street names are a telltale sign when pinpointing a location. Look out for suffixes and prefixes: ‘CALLE’ hints at Spanish-speaking countries, while ‘weg’ or ‘straat’ indicate Dutch areas. French regions commonly use ‘rue’. Norway often uses ‘...vei’ or ‘...veien’, while in Italy, ‘VIA’ is widely seen on signs. Finnish streets usually end in ‘...katu’ or ‘...ntie’, Danish in ‘...vej’ or ‘...gade’, and Swedish in ‘...gatan’ or ‘...vägen’. City names on Belgian signs can also be a big clue. Paying close attention to these linguistic cues is key to narrowing down your guess.', 'street_sign': "Street signs are crucial for determining locations in Geoguessr. Look for unique colors, shapes, fonts, and languages. Differences are key: from the USA's 'SPEED LIMIT' to Canada's checkerboard signs. Europe varies, with Ireland's yellow diamonds and Nordic countries' distinct warning signs. Blue directional signs might indicate the Netherlands or Nordic regions, but the specific style narrows it down. Look closely at pole materials, bilingual signs, and even the number of dashes on pedestrian crossings to make your best guess.", 'poles': "Utility poles vary globally and can help identify a country. Peruvian poles often have three arms. In Romania and Hungary, poles can have large holes going to the ground. Mexico's octagonal poles are indicative of the region. Taiwan's poles are cylindrical with distinctive diagonal stripes. Japan's poles feature unique vertical stripes. Malaysia's poles have black rectangles with white lettering, unique to the mainland. Polish poles have holes, but not reaching the ground. Thai poles have small vertical holes, resembling drill marks. South Korean poles exhibit diagonal stripes. In Mexico, a crucifix shape is common, while Belgium's square poles may resemble Thai designs. France and Spain have poles with indents, Spain's being whiter.", 'other': "Recognizing locations in Geoguessr can often hinge on small, seemingly mundane details. Peruvian houses typically feature distinct rectangular electricity counters, a telltale sign you're in Peru. In Puerto Rico, keep your eyes peeled for ubiquitous red and white 'Clasificados Online' signs. Such unique local elements can be the key to pinpointing your virtual whereabouts.", 'cars': "Cars can be key clues in pinpointing your location. For example, tuk-tuks suggest Peru in Latin America, as it's unique there. Pink taxis, often marked with 'CDMX' for Ciudad de México, are exclusive to Mexico City. Vehicle styles, taxi colors, and regional emblems on cars can help distinguish one place from another. Keep an eye out for these specific characteristics; they often signal not just a country, but sometimes an exact city.", 'buildings': "Buildings hold visual clues that can pinpoint your location. In identifying countries, look for specific architectural styles, materials, and unique house features. Andorra's buildings often showcase affluent, multi-storey gray stone work. Bermuda's homes stand out with semi-faded, bright paint and stark white roofs that match their window frames, blending with the sky. In Mexico, circular electricity counters on exterior walls and black water tanks atop houses are common. The Nordic countries have distinctive reddish-brown homes, while Greenland favors a palette of vivid colors.", 'flora': 'Flora is a key indicator in Geoguessr. Look for unique vegetation to pinpoint your location. Eucalyptus trees, for instance, suggest Australia. Terrain also aids in recognition; undulating landscapes separate Luxembourg and Norway from flatter regions like the Netherlands. Norway has more vegetation and varied terrain compared to Iceland, which features grassy landscapes sometimes punctuated by volcanoes and glaciers. Always notice the natural environment; it’s a big clue to where you are.'}


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

    # Create Categories
    update_categories()
    
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
        