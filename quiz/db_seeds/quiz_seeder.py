import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region, Category


CATEGORY_CHOICES = [
    ('coverage', 'Coverage'), 
    ('driving_direction', 'Driving direction'), 
    ('google_car', 'Google Car'), 
    ('language', 'Language'), 
    ('license_plate', 'License Plate'), 
    ('settlement_sign', 'Settlement Sign'), 
    ('bollards', 'Bollards'), 
    ('street_numbering', 'Street Numbering'), 
    ('street_markings', 'Street Markings'), 
    ('street_name', 'Street Name'), 
    ('street_sign', 'Street Sign'), 
    ('poles', 'Poles'), 
    ('other', 'Other'), 
    ('cars', 'Cars'), 
    ('pedestrian_crossign_sign', 'Pedestrian Crossing Sign'), 
    ('buildings', 'Buildings'), 
    ('flora', 'Flora'),
]

OPENAI_CONTENT = {'coverage': "Coverage refers to the presence and quality of Google Street View in a location. High coverage areas offer continuous, clear imagery while remote regions may show sporadic or outdated photos. Look for the stitching of images, presence of camera cars, and frequency of updates to gauge how well a country is covered. This can hint at infrastructure and the country's relationship with Google.", 'driving_direction': 'Driving direction is a key indicator in Geoguessr. Some countries drive on the right side of the road, while others on the left. Most of the world drives on the right, including the Americas, Europe, and China. Countries like the UK, Australia, India, and Japan drive on the left. Look for road signs, vehicles, and which side the steering wheel is on in cars to figure out driving direction.', 'google_car': "Spotting the Google car can be a big hint in GeoGuessr. Each country's Google car has unique features, like camera setups, antennas, or the car's make and model. Some countries have distinct camera mounts without the Google logo. The car's appearance might blend in more in certain regions, making it tougher to spot. Keep an eye out for subtle differences, as neighboring countries can use similar vehicles.", 'language': 'Language is a powerful hint for Geoguessr. Look for signs, billboards, and other text. Unique scripts like Cyrillic or Arabic can narrow down the region quickly. Languages with diacritical marks, like accents or tildes, can also be telltale signs. Notice the frequency of English use; it often indicates tourist areas or former British colonies. Pay attention to multilingual signs, as they can suggest border areas or regions with language diversity.', 'license_plate': 'License plates can be key clues when playing Geoguessr. Some countries have unique colors, size or plate formats. For instance, plates may display EU stars, be long rectangles or square shapes. Look for stickers, regional emblems or specific combinations of letters and numbers. Check if the plate is front, back, or both. These details narrow down possible locations and help distinguish between countries with similar-looking plates.', 'settlement_sign': 'Settlement signs often hold key clues. Look at the language, font, and color scheme. Many countries have unique sign designs or languages. For example, Cyrillic script might suggest Eastern Europe, while unique alphabets could point towards countries like Greece or Georgia. Notice if the sign has decay due to weather, as this might indicate a specific climate zone. Urban signs often differ from rural ones, with more logos or English usage in tourist areas.', 'bollards': "Bollards come in various shapes, colors, and designs, and can offer clues about your location. While their primary purpose is to control or limit vehicle access, the style of bollards can suggest a country's design preferences or security concerns. Noticeable features include color—red and white might signal Europe, while yellow is common in the Americas. Reflective tape, unique shapes, and whether they're permanent or temporary can also hint at the location. Pay attention to their context—near landmarks, in urban or rural settings, they can provide valuable clues.", 'street_numbering': 'Street numbering systems can be a key indicator of your location. Sequential numbering suggests a grid-like city plan, often seen in the Americas. Odd and even numbers on opposite sides of the road are common globally. In contrast, the absence of visible street numbers or chaotic numbering might hint at older European cities or certain Asian countries. Look for consistency in signage, the style of numbers, the presence on buildings vs. poles, and any accompanying street or district names, as these often reflect local language and conventions.', 'street_markings': "Street markings are key in pinpointing your location. Look for colors used on road lines; yellow often means the Americas, white for Europe and other regions. Patterns matter, like zebra crossings or specific shapes for stop lines and arrows. Also, notice whether text is on the road, like 'BUS STOP' or 'SCHOOL'—language can be a giveaway. Texture changes at intersections and unique markings for lanes or no-entry zones help too.", 'street_name': "Street names can give away the country's identity. Look for language patterns, unique characters or accents. Some countries have street signs in multiple languages, reflecting their diverse cultures or historical influences. Consider the format too; some places have numbered systems while others have long, descriptive names. Street naming conventions vary widely, but recognizing the local language and script is your best hint.", 'street_sign': 'Street signs can provide vital clues in Geoguessr. Notice the shape, color, and language of the sign. Some countries use unique fonts or feature regional languages. Look out for unique alphabets, like Cyrillic or Japanese, and shape differences, like the red triangle for warnings in the UK. Reflective quality can hint at affluence and thus narrow down possibilities. Remember, road signs in Europe often appear standardized but may have language-specific details.', 'poles': 'Utility poles vary by design and markings, offering clues to your location. Different countries use distinct materials, pole designs, and even the arrangement of wires. Look for unique identifiers like company logos, warning signs, or specific construction methods used for the electric poles; these can sometimes be linked to regional standards or practices. However, remember that certain styles might be found across neighboring countries, so use poles as one of several clues to pinpoint your location.', 'other': "Recognizing a country in Geoguessr often hinges on spotting unique features. Check for road markings, language on signage, architectural styles, vegetation, and car license plate formats. Even the sun's position can hint at whether you're in the northern or southern hemisphere. Compare these clues with your general knowledge to narrow down the possibilities.", 'cars': "Cars can provide crucial clues. Look for the side of the road they drive on, unique car models, and bumper stickers. License plate designs can also hint at the country, but remember, they are often blurred in Geoguessr. Notice any distinctive vehicle signage like country-specific warning signs; for example, distinctive shapes or colors of number plates, or stickers that indicate the country of origin. Also, pay attention to the condition and styles of vehicles as they can reflect the region's economic status.", 'pedestrian_crossign_sign': 'Pedestrian crossing signs are a quick visual cue to pinpoint a country in Geoguessr. Look for unique shapes, colors, and symbolic representations. While a walking figure is universal, the design varies: some signs are triangular or circular, have flashing lights, or distinctive patterns. Differences in the depiction of the pedestrian, from detailed to abstract, can also be a hint. Consider the context too; urban settings might have additional local language or symbols. Always pay attention to the overall road signage design language for regional clues.', 'buildings': 'Buildings can provide critical clues in Geoguessr. Look for architectural styles, construction materials, and any visible signs or placards. Unique designs or colors may indicate a specific region or country. Roof shapes vary, with gabled roofs common in Europe and flat roofs in arid regions. Building height and age can also be hints; high-rises might suggest a developed urban area, while traditional huts could point to rural African or Asian locales. Modern, glassy structures could suggest wealthier nations. Safety barriers and construction styles can further narrow down your guess.', 'flora': 'Flora can be a strong hint for identifying countries in Geoguessr. Look for unique vegetation types like palm trees suggesting tropical climates or baobabs indicating Madagascar or parts of Africa. The presence of specific tree species like eucalyptus hints at Australia, while olive trees are common in the Mediterranean. Plantations can also give clues: tea estates are common in India and Sri Lanka, while vineyards may indicate European countries like France or Italy. Notice the state of flora too; lushness may indicate a wet climate, while sparse vegetation suggests arid areas.'}


def update_categories():
    # Create Categories
    for input_category in CATEGORY_CHOICES:
        print(">>>>>>>>>")
        print(input_category)
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
            db_category.delete()
            log.info(f"Category {db_category.name} deleted")


def update_quizzes():

    # Create Categories
    update_categories()
    
    # Category Quizzes

    # Creat category quizzes
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
        log.info(f"Quiz {quiz_name} updated")
    
    # Delete old category quizzes
    db_quizzes = Quiz.objects.filter(category__isnull=False)
    category_names = [category.name for category in categories]
    for db_quiz in db_quizzes:
        if db_quiz.name not in category_names:
            db_quiz.delete()
            log.info(f"Quiz {db_quiz.name} deleted")
    

    # Country Quizzes
    # Create one quiz for each Country region 
    
    # Get distinct regions from Country objects that are not empty strings
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

        log.info(f"Quiz {quiz_name} updated")
    
    # Delete old country quizzes
    db_quizzes = Quiz.objects.filter(category__isnull=True)
    region_names = [region.name for region in regions]
    for db_quiz in db_quizzes:
        if db_quiz.name not in region_names:
            db_quiz.delete()
            log.info(f"Quiz {db_quiz.name} deleted")
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        
        # Delete quiz if no facts
        quiz = Quiz.objects.get(uuid=quiz.uuid)
        if quiz.num_facts == 0:
            quiz.delete()
            log.info(f"Quiz {quiz.name} deleted")
        