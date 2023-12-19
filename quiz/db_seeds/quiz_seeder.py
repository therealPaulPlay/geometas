import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region, Category


CATEGORY_CHOICES = [
    ("coverage", "Coverage", "Coverage refers to the extent and quality of Google Street View available in a location. Countries with comprehensive coverage have numerous and frequently updated Street View images, making landmarks and signage clearer and more recognizable. In contrast, countries with limited or no coverage might only have images from major cities or tourist areas, often dated, lower in resolution, or completely absent. Recognizing coverage patterns helps narrow down possible countries. When in a high-coverage area, expect detailed road networks and street-level imagery. In places with spotty coverage, rely on other clues like landscape, architecture, or vehicles."),
    ("driving_direction", "Driving direction", "Identifying a country by the side of the road on which vehicles drive is a key clue in GeoGuessr. Countries like the UK, Australia, and Japan drive on the left, while most others drive on the right. Consider other factors that may corroborate your guess, such as car models, road markings, and sign languages, because some regions have countries with both driving directions. Always scan for other vehicles, as the driver's position inside can confirm the correct side. Busier roads often have clearer signs of correct flow direction."),
    ("google_car", "Google Car", "Recognizing a country by the Google Street View car can be quite telling. Some countries have unique camera mounts or the car models differ. Look for unusual attachments on the car, logos, or the type of equipment used. Certain countries have off-road setups for rural areas. Sometimes, you might not see the car itself but its shadow. Pay attention to the shape of the shadow, as it can indicate the type of vehicle used. Also, notice any blur on the car; some countries mandate blurring to obscure the car's details. Remember, however, that car types can change over time, so it's not always a definitive clue."),
    ("language", "Language", "The Language category is incredibly useful in Geoguessr to identify locations. Pay attention to the script on signs - Cyrillic is used in Russia and some neighboring countries, while unique characters might indicate Japan or Korea. Don't forget about regional languages or bilingual signs, which can hint at autonomous regions or countries with multiple official languages. Consider also the prevalence of English; it's common in tourist areas worldwide but less so in rural regions of non-English speaking countries. Language clues are often key to narrowing down your geographic guess."),
    ("license_plate", "License Plate", "License plates are a unique identifier for vehicles and can be a great clue in Geoguessr. Colors, text format, and symbols can hint at a country's identity. Some countries have highly distinctive plates, like unique color schemes or emblems. Others might look alike, so check for fine details, like regional codes or special characters. European plates often have blue bands with the EU flag and country initials, while South American plates might show country-specific colors and symbols. The key to mastering this category is observation and learning the little differences that can set similar-looking plates apart."),
    ("road_lines", "Road Lines", "Road lines can be crucial in pinpointing your location in Geoguessr. Different countries adopt various colors and patterns for road markings which can be distinguishing factors. Look out for continuous and broken lines, their colors, whether they're double or single, and the presence of any unique patterns or symbols. Yellow center lines are common in North America, while white is the standard in many European and African countries. Patterns like zebra crossings and arrows also vary, with some countries having distinctly shaped or colored variants. Texture and state of disrepair can hint at less maintained roads in certain regions. Remember, similar practices can be found in regions with shared transportation standards or historical ties."),
    ("settlement_sign", "Settlement Sign", "Settlement signs offer clues about your location. Look for language, fonts, and colors as they often follow national standards. Many countries have unique shapes or emblems on their signs. For example, in Europe, settlement signs are often white with black or blue lettering, and have distinct shapes by country. Colors vary widely, some with red borders or background. Also, the material or aging of the sign can hint at the local climate and maintenance, hinting at richer or poorer countries. Scrutinize any additional symbols or graphics, as they may point to regional or country-specific features."),
    ("bollards", "Bollards", "Bollards are key visual clues in Geoguessr, helping to pin down locations. Each country often has distinct bollard designs. Look for characteristics such as shape, color, reflector patterns, and additional markings. For example, Eastern European countries like Hungary and Bulgaria have white rectangles on bollard backs, while Serbian bollards have asymmetrical red shapes. In contrast, Turkish bollards are slightly fatter. Recognize Czech and Slovakian locations by fluorescent orange stripes on bollards, while Ukrainian ones have a distinctive larger red rectangle. Polish bollards feature red diagonal stripes. Italian bollards are marked by a vertical red rectangle inside a black diagonal strip. Finnish and Icelandic bollards are cylindrical or yellow, respectively. Austrian bollards' dark reflectors are unique, and South African signs act as their bollards. By noting these differences, players can use bollards as valuable geographic hints."),
    ("street_numbering", "Street Numbering", "Recognizing a country by street numbering can be subtle, but there are clues. In some places, numbers are sequential, while others use the 'hundreds' system where the number corresponds to the nearest cross street. Some countries use even numbers on one side, odds on the other. Look at the style and formatting of the numbers; font type, presence of a number plate, or etched on buildings can hint at the region. Consistency and maintenance level of the street numbers often reflect the country's infrastructure quality. Countries may also have unique color codes or signs for indicating address numbers."),
    ("street_markings", "Street Markings", "Street markings are a crucial clue in GeoGuessr. Each country has unique road marking styles, so watch for color, pattern, and text. Most markings are white or yellow, but colors like blue or red can signal specific countries or regions. Double lines often mean no passing, and arrows point to direction or lanes. Textual markings, for example, 'STOP' or 'BUS', can indicate language and thus narrow down the region. Additionally, crosswalk styles and the presence of bike lanes can be major tips. Look for these details and compare them with the side of the road traffic drives on to improve your guessing game."),
    ("street_name", "Street Name", "Street names can be a vital clue in pinpointing your location in Geoguessr. They often reflect language, history, and cultural influences. For instance, a 'Calle' or 'Avenida' might suggest a Spanish-speaking country, while a 'Rue' signals French influence. Look out for language-specific characters like ñ, ç, or umlauts, which are unique to certain languages. Additionally, street signs' color and shape can hint at regional standards—blue signs might be found in Europe, for example. Consider if the street name includes a person or place, as this can be indicative of local heroes or significant historical events tied to a specific area. Lastly, the presence of English streets in a non-English-speaking country could point to popular tourist areas or former British colonies."),
    ("street_sign", "Street Sign", "Street signs provide great clues for pinpointing your location. Each country has a unique street sign design that can include shape, color, typography, and language. Look out for color patterns; for instance, blue signs are common in Europe, while the U.S. favors green. Typography can hint at the region, with certain fonts being distinctive in places like Scandinavia. Sign shapes vary too; triangular for warnings in many countries, with variations in design. Additionally, the presence of multiple languages on a sign can be a giveaway for specific countries."),
    ("poles", "Poles", "Utility poles can be quite revealing when you're pinpointing locations. Each region may have a distinct style or configuration. Look for the materials used: wooden poles are common in North America and parts of Scandinavia, while you might see more concrete or metal in Europe and Asia. The design of the top of the pole, such as the number and arrangement of crossbars or the presence of transformers, could hint at the local climate or the engineering standards of the country. Pay attention to the cables; densely wired poles might indicate urban areas. Even the height and thickness can be clues, as can any writing or markings on the poles. These details are subtle but crucial in narrowing down countries in Geoguessr."),
    ("other", "Other", "The Other category in country identification could refer to features that don't fit into standard meta categories. Look for unique elements like boundary stones, mile markers, or distinct environmental conservation signs. It could also indicate less common infrastructures such as local shrines, atypical road signs, or peculiar utilities. You might encounter seasonal decorations or community-specific messages. If it feels out of the ordinary, it\'s probably a valuable clue. Remember, unusual features can be the most revealing, so pay close attention to even the smallest details."),
    ("cars", "Cars", "Recognizing countries in Geoguessr through car details can be a game-changer. First to note are license plates. Some countries have highly distinctive plates, such as the EU strip or unique color schemes and fonts. Car models can also hint at the location - specific brands may dominate the roads regionally. Don't overlook the side of the road cars are driving on; it narrows down possible countries significantly. Finally, car condition can reflect local climate and economic status, potentially narrowing down your guesses."),
    ("pedestrian_crossign_sign", "Pedestrian Crossing Sign", "Pedestrian crossing signs are a key visual clue to identify a location. They vary in design, color, and format worldwide, offering subtle hints about where you might be. For instance, some signs display detailed human figures while others are more abstract. Color schemes can range from the common white-on-blue to yellow or even neon hues. The shape of the sign is also a tell-tale sign – from the regular triangles and circles to unique silhouettes. Look for text on the signs; it often indicates the local language and can narrow down the geographical area. Reflectivity and sign condition may suggest a country’s investment in road infrastructure, which correlates with economic status."),
    ("buildings", "Buildings", "Buildings have unique styles that vary significantly by region. Check for architectural designs like roofs, doors, windows, and the materials used. Modern, glass skyscrapers could suggest a developed, urban area, often associated with wealthier countries. Traditional buildings with unique features might indicate a historical region. Roof styles, such as thatched or tile, can tell a lot about local materials and climate. Pay attention to building colors, as some regions have a characteristic palette. Identifying specific construction techniques can be a clue to the local geography and culture. Remember, places with a colonial past might have European-influenced architecture."),
    ("flora", "Flora", "Flora varies greatly around the world, but some elements can hint at a country's location. Tropical countries often have lush, dense greenery with large-leafed plants and vibrant flowers. If you notice olive trees or shrubs, you might be looking at a Mediterranean climate. Countries towards the poles have coniferous forests. Another clue is farmland crops; rice paddies are distinctive to Asia while vast wheat fields might indicate North America or Russia. Always pay attention to the types of trees, plants, their arrangement, and the overall landscape. Unique flora like baobab trees in Madagascar or eucalyptus in Australia can be dead giveaways."),
]


def update_categories():
    # Create Categories
    for input_category in CATEGORY_CHOICES:
        category_db = Category.objects.filter(slug=input_category[0]).first()
        if category_db:
            category_db.name = input_category[1]
            category_db.save()
        else:
            Category.objects.create(
                name=input_category[1],
                slug=input_category[0]
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
        