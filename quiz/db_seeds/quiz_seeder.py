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

OPENAI_CONTENT = {'coverage': "Recognizing Geoguessr locations by coverage clues starts with unique traits: Costa Rica features pathways instead of drivable roads, making it impossible to move off the path. Finland stands out in the Nordics with its dirt or gravel roads. A low Street View camera sets Switzerland and Japan apart, offering a closer-to-the-ground perspective; keep an eye out for a similar effect in Sri Lanka and Taiwan. Montenegro and Albania may have a noticeable split in the sky upon panning upwards. Uganda's Street View is concentrated around Kampala with distinctive red soil, a feature shared with parts of Kenya.", 'driving_direction': "If you're trying to determine the location in Geoguessr by driving direction, notice that vehicles drive on the left in a few distinct places. In Bermuda, look for a single, yellow center line; in Malta, the Mediterranean scenery sets it apart from other left-driving European countries like the UK and Ireland; and in the US Virgin Islands and Eastern Russia, left-hand driving contrasts with their regions' norms. The Northern Mariana Islands and American Samoa are unique for island regions, with driving on the right, while Rwanda's right-side driving differs from its neighbors Kenya and Uganda, who drive on the left. Recognizing these driving patterns along with the local scenery can be key clues to pinpointing your location.", 'google_car': "Recognizing Geoguessr locations by vehicle metas involves looking for unique features of the Google Street View car that vary by country. For instance, in Kenya and Mongolia, look for a snorkel on the car. In Senegal, the Street View car often has a visible roof rack or silver truck cab. The Faroe Islands are identifiable by a grey roof rack on a car in a jagged, treeless mountain landscape. Chile's identifier is the white rear of the car, and Guatemala has visible bars and black mirrors. Sri Lanka's car has distinct blue, white, and red stripes, while South Africa and neighboring countries often have a white car. Mongolia has a 'camping equipment' look under the car. Ecuador's Street View car has a short antenna, Rwanda uses a black truck, and Argentina and Uruguay's car fronts are ghostly black. Vietnam's coverage uses a motorbike, Ukraine features a red car with a long antenna, and the Dominican Republic has bars with black lines. Qatar uses a white car, Tunisia has a following green Mazda, and Nigeria may have a 4-wheel drive escort. In Panama, look for a unique antenna, and Bermuda has a black truck that's sometimes blurred. Germany's recent coverage should show a blue tinge on the car, Iceland's will have an aerial, and Eastern Europe usually features an aerial, except for Serbia and North Macedonia. Lastly, keep an eye out for vehicle variations in American Samoa, Christmas Island, Guam, South Africa, and the Northern Mariana Islands.", 'language': "When playing GeoGuessr, identifying languages can be a massive clue to pinpoint your location. Unique characters or alphabets often give away specific countries. For instance, Slovakia's use of Ľ, Ô indicates you're likely there, while Ř, Ě in Czechia can place you in Czech Republic. Sinhala's 'C' shaped letters are a telltale sign of Sri Lanka. Hindi's backward 'h' and 'F' shapes single out India, and Arabic's calligraphic style spans across the Middle East and Northern Africa. In East Asia, complex characters with more strokes suggest China, while Korean's distinct combination of circles and blocks stands out. Identifying European languages hinges on specific diacritics like the Norwegian and Danish ø, the German umlauts (ä, ö, ü), Hungarian's ő and ű, and the Romanian ş and ț. Cyrillic alphabets with unique letters can clue you into places like Macedonia, Serbia, Ukraine, and Bulgaria. While recognising the specific end-vowel pattern can signal you're in Italy, and the 'ij' pair hints at the Netherlands. Paying attention to these language metas can dramatically improve your country-guessing game.", 'license_plate': "When playing Geoguessr, recognizing locations by license plates can be a game-changer. In the US, the absence of a front license plate often points to the south-eastern states, including Michigan and Arizona. In Asia, Malaysian plates are notably black with white text, while the Philippines presents green and white variations, and Indonesia has a distinct tripartite black and white layout; Japan and Israel sport yellow plates, whereas Senegal and Ukraine feature blue. European clues range from Italy's blue stripes and Portugal's yellow stripe to Belgium's faint red lettering and Croatia's transition from white to blue-striped plates. Africa offers yellow plates across multiple countries, including Ghana and Kenya. Notice the subtle geographic influences, like flatter landscapes for the Netherlands, or wider plates in Brazil compared to other Latin American countries. Understanding these nuances can significantly improve your country identification skills in Geoguessr.", 'bollards': 'In Geoguessr, recognizing bollards can provide vital clues to the country you\'re in. Serbian bollards are distinguished by a unique red rectangle on one side, while Czech and Slovak bollards stand out with fluorescent orange stripes. Distinct Polish bollards feature a red diagonal stripe, whereas Russian bollards are identifiable by a narrow support pole, setting them apart from often dilapidated Ukrainian counterparts with wider red rectangles. Finland\'s cylindrical bollards are a Nordic outlier, and Italian bollards are recognizable by a red rectangle inside a black diagonal strip. In contrast, Austrian bollards have black or dark red reflectors with a distinctive "black hat." Unconventional shapes such as the cigarette-like Peruvian and "match-like" Cambodian bollards, or the yellow-topped Icelandic ones, offer unique visual cues. In the Baltic region, Lithuanian bollards mimic wood with an orange rectangle, Latvian bollards present a thin profile with white circles on the back, and Estonian bollards are cylindrical with white or yellow rectangles. Observing these details will help pinpoint your location in the game.', 'street_markings': "Recognizing street markings can be a game-changer in GeoGuessr, as they often give subtle hints about your location. Look out for distinctive features like Chile's all white or yellow road lines, Denmark's unique short-dashed edge markings, or South Africa and its neighbors with yellow side and white center lines. Russia and Guatemala use numbers on their road markers to indicate distance—a high number in Guatemala hints at a northern location. Ireland's yellow dashed edge lines are a telltale sign differentiating it from the U.K. France's long white side dashes, Norway's white side lines with longer dashes than gaps, and Sweden's unique dash-to-gap ratio are key identifiers in Scandinavia. Spain's guardrails have yellow-orange reflectors not seen elsewhere in Europe. Corsica's short dashes and Mediterranean landscape, Iceland's dark roads with grassy edges, Finland's yellow and white road lines, Greece's double white center lines, and Rwanda's high-quality paved roads with yellow center lines are all important cues to keep in mind.", 'street_name': 'Knowing street name metas is key in Geoguessr to identify locations. Spanish-speaking countries use "CALLE," Dutch areas have "weg" and "straat," and French regions show "rue." Norway\'s streets include "vei" or "veien," Belgium often incorporates city names, and Italian signs have "VIA." In Finland, look for "katu" and "ntie," while Danish and Swedish streets end in "vej," "gade," "gatan," and "vägen." Vienna has unique blue signs, Hungary uses "UTCA," Croatian signs are blue with "ULICA," and "Triq" is typically Maltese. Brazil\'s highways start with "BR," and Russia\'s road numbers have prefixes. New Zealand uses blue or green street signs contrasting Australia\'s white. Rwanda\'s Kigali has street signs with "KG," "KN," or "KK," indicating the road\'s importance by the number of digits.', 'street_sign': "Understanding street signs is a savvy way to tease out your location in Geoguessr. They are like a secret language hinting at which part of the globe you've been dropped into. For instance, the design, color scheme, and language are tell-tale signs that you should watch out for. In the USA and Canada, distinct scripts on speed signs and unique sign colors respectively can clinch the deal. In Europe, the shape of warning signs can vary significantly – from triangular with thick red borders to yellow diamonds in Ireland. Language is another giveaway; for example, bilingual signs in regions like New Brunswick or Brittany can pinpoint your location. Road markers and the orientation of signs, seen in countries like Romania and the Baltics, also offer clues. Every detail, from the manner of script - be it Cyrillic or Latin - to the color and shape of highway shields, as seen in Australia and New Zealand, plays a critical part in unraveling the mystery of your whereabouts. Remember, it's all about noticing those small yet significant differences.", 'poles': "Recognizing utility poles can vastly improve your Geoguessr game by pinpointing countries and regions. Look for distinct characteristics like the three-armed poles in Peru or the octagonal shapes common in Mexico. Taiwanese poles often feature striking black and yellow diagonal stripes, a pattern echoed with variations in Japan and South Korea. Malaysian poles are identifiable by black rectangles with white lettering, exclusive to the mainland. In Thailand, small vertical drilled holes are a giveaway. While Romania, Hungary, and Poland share concrete poles with holes, Romanian poles often have a yellow mark and the holes extend to the ground, distinguishing them from Polish ones that stop short. Baltic states have variations of 'pine cone' features on their poles. In Australia, Tasmania's poles can have olive metal wraps, and South Australia uses unique Stobie poles. New Zealand has silver or white wraps. Each country has its own subtle but distinct pole style, which can be a crucial clue for location in the game.", 'other': "Recognizing Geoguessr locations based on country meta information involves identifying unique features: Peru has distinctive electricity counters, while Puerto Rico has red and white 'Clasificados Online' signs. Hungary is notable for its special fire hydrants, and Croatia has narrow blue ones. Bulgaria's landscape features Eiffel-like towers, and Serbia uses the '.rs' internet suffix. In Uganda, armed figures may follow the Google Street View car. Botswana boasts high-quality main roads and a flat landscape. Midway Atoll is distinguished by numerous albatross chicks, and on Christmas Island, the presence of red crabs and a person's blurred outline carrying the Street View camera is characteristic.", 'cars': "In Geoguessr, spotting unique cars can vastly improve your location-guessing skills. For instance, Tuktuks are distinctive three-wheeled vehicles which, within Latin America, are only found in Peru, providing a clear indicator of your whereabouts. Similarly, pink taxis are a dead giveaway for Mexico City, as they're a city-specific feature. So, if you come across a pink taxi, it's safe to bet you're in the heart of Mexico. Keep an eye out for 'CDMX' signage too, as this acronym is a direct reference to Mexico City and can confirm your guess.", 'buildings': "Recognizing buildings can be a key indicator in Geoguessr to pinpoint your location. In Andorra, look for multi-storey stone buildings. Bermuda's buildings stand out with white roofs and brightly painted walls. Mexico frequently has circular electricity meters and black water tanks visible outside houses. Nordic homes may show a reddish-brown color, while Greenland houses are notably colorful. Swiss buildings often feature numerous window shutters and wooden construction. In the Baltic countryside, expect to see houses with corrugated iron-like roofs. Brazil's transparent satellite dishes are distinctly recognizable. Lastly, high property walls are a strong indicator of being in Rwanda's capital, Kigali.", 'flora': "Recognizing locations in Geoguessr through flora involves noting the unique vegetation and landscape features of each area. Eucalyptus trees signal Australia, while gentle slopes and green grass fields indicate Luxembourg. Norway's hilly, mountainous terrain with more vegetation differs from Iceland's flat landscapes with limited vegetation, except for grass, and visible volcanoes and glaciers. Switzerland's towering mountains are often accompanied by wooden, multi-storey houses with terracotta roofs. Ukraine and Russia are known for trees with white-painted trunks. Malta's scenery features low-lying vegetation and rock walls, whereas in New Zealand, mountains looming in the distance might mean you're on the South Island. Tasmania or Victoria in Australia are characterized by rolling hills. Eswatini and Lesotho are both hilly and surrounded by South Africa, but Eswatini has more trees, while Lesotho is largely treeless except in the north.", 'guardrails': "In Geoguessr, recognizing guardrails can significantly narrow down your location. Lithuania's guardrails stand out with orange reflectors, while Latvia's feature red and white ones, and Estonia's lack reflectors altogether. The unique B-profile guardrails with 90-degree angles and a narrow center are your clues for Croatia, Serbia, Poland, Denmark, and certain areas of Turkey, North Macedonia, Ireland, and Germany. If you spot a guardrail with a wide central section that can fit three top sections, you're likely in Czechia or Slovakia. These details are key visual cues when pinpointing your location in the game."}


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
        