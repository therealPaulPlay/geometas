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
    ('chevrons', 'Chevrons'),
    ('milestones', 'Milestone Markers'),
    ('signposts', 'Sign Posts'),
]

OPENAI_CONTENT = {'coverage': "Recognizing Geoguessr locations by Street View coverage involves noting unique characteristics: you can't leave the footpath in Costa Rica, gravel roads may indicate Finland, and sky rifts suggest Albania or Montenegro. In Nigeria, a following police car is usual, Uganda features red soil and limited to Kampala, while Kenya shares similar soil color. India's coverage appears foggy due to low-quality cameras. Hong Kong stands out with skyscrapers and bayside Chinese signs. Monaco's lavish harbors, yachts, and mountain backdrop are distinctive, as is Madagascar's trekker coverage in the country's central region.", 'driving_direction': "Recognizing the correct side of the road vehicles drive on is a crucial meta clue in Geoguessr. Places like Bermuda, the US Virgin Islands, Malta, and the UK & Ireland drive on the left, with Malta's Mediterranean look being distinctive. Eastern Russia has right-hand steering wheels, unlike Western Russia. The Northern Mariana Islands have a tropical vibe and right-side driving, uncommon for islands. In contrast, Rwanda, American Samoa, Cambodia, the Philippines, Laos, and Vietnam drive on the right, with Cambodia standing out in Southeast Asia and American Samoa featuring double yellow lines and denser coverage on Tutuila Island.", 'google_car': "Recognizing Geoguessr locations through Google Street View car details greatly improves your game strategy. The appearance of the Google car varies widely by region, offering clues to pinpoint the country. For example, in Kenya, a snorkel on the car indicates you're likely there. The Faroe Islands display a distinct landscape with cars carrying grey roof racks. In South America, Chile and Ecuador each have unique car features: a white rear and a stubby antenna, respectively. Sri Lanka has a car painted with blue, white, and red stripes, while Uganda features white edges with black mirrors. Notably, Vietnam's coverage comes from a motorbike, a significant outlier. Various antenna designs, roof racks with specific patterns, and unique car silhouettes such as trucks or blurred images are distinguishing factors in various countries. These details are sometimes subtle but often the key to unlocking your virtual location.", 'language': "Recognizing languages can be a powerful tool in GeoGuessr to pinpoint your location. For example, Slovak has unique letters like Ľ, Ĕ, while Czech has Ř, Ě. Sinhala resembles backwards 'C' shapes, and Hindi uses characters that look like upside-down 'h'. Arabic script has a calligraphic style with line accents, and Chinese characters are complex with more strokes than Japanese or Korean. Cambodian features right-pointing hooks, and Hebrew has a distinct blocky script. Japanese uses simpler strokes and characters like ノ, whereas Thai features circles at symbol ends, contrasting the curved nature of Lao script. Korean is identifiable by its use of circles and a rigid, blocky appearance. In Europe, Dutch is notable for 'ij', 'z', 'w', and double vowels, while Italian often ends words with vowels. German includes umlauts and the eszett 'ß' (except in Switzerland), and Nordic languages have unique diacritics like ä, ö, å, and double letters in Finnish. Cyrillic script variations mark languages like Macedonian, Bulgarian, Ukrainian, and Serbian, each with their own unique letters. Romance languages such as Romanian have special letters like ă, ș, and ț. Spotting these nuanced writing systems and character uses can be the key to correctly identifying your GeoGuessr location.", 'license_plate': "Recognizing locations in Geoguessr through license plates involves spotting distinct features like color patterns, presence or absence of specific stripes, shapes, and characters. For example, US southeastern vehicles might lack front plates, a commonality up to Michigan and over to Arizona. Malaysian and Indonesian plates both have black backgrounds but differ in the number of white text blocks. European plates often have a blue stripe on the left, but countries like Switzerland and Iceland deviate with unique identifiers. Russia and Ukraine have completely white or yellow plates for commercial use. Many Asian countries vary from elongated to nearly square plates, and colors range from Japan's frequent yellow to India's special green for electric vehicles. South American variations include the recognizable orange commercial vehicle plates in Brazil and the blueish hue in Bolivia. By noting these nuances, players increase their chances of pinpointing the correct location.", 'bollards': 'Recognizing bollards can significantly boost your location identification accuracy in Geoguessr. European bollards often have distinct shapes, colors, and reflective markers that vary from country to country. For instance, Serbian bollards feature asymmetric red rectangles, and Croatian ones have identifiable front and back color patterns. Likewise, in the Nordic regions, Finnish bollards stand out with their cylindrical shape. Telling countries apart in Eastern Europe can hinge on details like the wear and tear of Ukrainian bollards or the unique color stripes on Czech ones. Down under in Australia, bollard designs differ with red rectangular features, while in Asia, Japanese bollards display characteristic shapes and colors. In the Americas, be on the lookout for the cigarette-shaped design in Peru and the notable Ecuadorian consistency in style. By paying close attention to these subtle differences, you can vastly improve your chances of pinpointing the right location.', 'street_markings': "Street markings can be a vital clue in Geoguessr to pinpoint your location. For instance, Chile's all-white lines and occasional all-yellow can set it apart in South America. Denmark's short-dashed edge markings are unique, while Russia's blue road markers display distances. Iceland boasts dark-colored roads with white, dashed edges and grass right up to the pavement. Guatemala's signs indicate distance from Guatemala City, aiding in north-south orientation. France's long white side dashes are a standout feature in Europe, contrasted by Ireland's yellow dashed edges. Norway is known for yellow center and white side lines, while Swedish side dashes have longer gaps than actual lines. Spain's guardrails with yellow-orange reflectors, Corsica's shorter white dashes, and Greek double white center lines offer regional specificity. In Asia, Malaysia's thick, yellow perpendicular lines and black-and-white curbs in Qatar are indicative. Argentina's white and yellow lines, Uruguay's distinctive triple lines, and Czechia's solid outer lines with no center line help narrow down locations. Poland's double middle lines, Brazil's double yellow center with white outer lines, and Rwanda's often faded yellow and white lines provide additional geographical hints. Recognizing these distinct patterns can be the key to accurately guessing your location.", 'street_name': 'Recognizing street names is a powerful tool in Geoguessr for pinpointing locations. Look out for distinct prefixes and suffixes that give away the country: "BR-" in Brazil, "M", "A", or "P/R" in Russia, "CALLE" for Spanish-speaking areas, "weg" and "straat" in Dutch, "katu" and "ntie" in Finnish, and "rue" in France. Vienna, Austria, is unique with blue street signs, while Norway uses “…vei” or “…veien”. In Belgium, the city name features on the sign, "VIA" is common in Italy, "…vej" and "…gade" in Denmark, "…gatan" and "…vägen" in Sweden, “utca” in Hungary, "Ulica" in Croatia, and “Triq” in Malta. New Zealand sports blue or green street signs, contrasting Australia\'s white. Rwanda uses "KG", "KN", or "KK" prefixes in Kigali, and Ankara, Turkey, has a distinctive curved sign. Look for “вулиця” or "вул." in Ukraine, while in Eswatini and Lesotho, green signs with white text and yellow numbers are commonplace, starting with "MR" and "A" respectively.', 'street_sign': "Recognizing street signs is key in GeoGuessr to pinpoint your location. Each country has unique characteristics: Singapore favors pale green signs with bold fonts, while in Denmark, they are white with metal borders. Spain's pedestrian signs stand out with eight dashes, and Polish warning signs feature yellow backgrounds and thin red outlines. Canadian signs often have bilingual text, supported by wooden or metal posts. Icelandic signs are distinct with their yellow backgrounds, and Scandinavian countries typically use blue or green for directional signs. France is known for 'D' road signs, Austria for 'EINBAHN', and in the Baltics, you'll observe different border styles on warning signs. Australia differentiates regions by pole color. Meanwhile, Southeast Asia has yellow diamond warning signs, with localized variations like Cambodia's white outline. Distinguishing regional differences, such as bilingual signs in Finland or Croatia's yellow directional signs, is also helpful. Japanese signs tend to have red and white arrows, whereas in Latin America, coloration and mounting styles vary, with black and yellow stripes in Uruguay. In Middle Eastern countries like Israel and Qatar, signs often include multiple languages. Navigating GeoGuessr with these meta insights on street signs vastly improves location identification.", 'poles': 'Recognizing utility poles can be a major clue in GeoGuessr. Different countries and regions have distinct styles, such as Peru\'s triple-arm poles, Hungary\'s "holey poles," Mexico\'s octagonal or crucifix-shaped poles, or Malaysia\'s poles with black rectangles and white lettering. Taiwan, Japan, and South Korea poles have black and yellow stripes, varying in how far they extend. Belgium, Thailand, and Romania feature poles with holes or indents, while Bulgaria\'s resemble the Eiffel Tower. In the Baltics, look for different pole shapes and \'pine cone\' attachments. Australia and New Zealand have unique metal wrappings, while African countries like Nigeria and Ghana have specific indents or wooden poles. South America features ladder-like poles in Brazil and distinctive shapes in Uruguay, while octagonal poles are exclusive to Colombia. Knowing these features helps narrow down your GeoGuessr guess to the correct country or even region.', 'other': "When pinpointing Geoguessr locations, observe local nuances: Peru's rectangular electricity counters; Puerto Rico's 'Clasificados Online' signs; Hungary's red fire hydrants; Serbia's '.rs' domain; Croatia and Botswana's distinct fire hydrants and roads respectively; Uganda's armed escorts; Midway Atoll's albatrosses; Christmas Island's red crabs; Turkey's wide roads; Indonesia's TV dishes and 'PT' company signs; Bangladeshi red and white bollards; Colombia's wooden fences; India's traditional attire; Galapagos's limited coverage with tortoises; Philippines's concrete block roads; Jeju's rock walls; Argentina's street trees and YPF gas stations; Brazil's BR Petrobras stations and transparent dishes; Ukraine's blue and yellow street items; Malaysia's 'Sdn Bhd' signs; and Lesotho's Basotho blankets. These details are vital clues to the right location.", 'cars': "Recognizing cars is crucial in Geoguessr for pinpointing locations. Tuktuks are a giveaway for Peru in Latin America, while pink taxis indicate Mexico City. In Colombia, taxis showing license plates on the side often reveal their city. The Philippines features distinctive mini buses and rickshaws, similar to those in Bangladesh, where vehicles drive on the left. Hong Kong is identifiable by its green and red taxis. Japan's cars often have a unique, boxy design, which sets them apart from vehicles in other countries. Pay attention to these vehicle features to improve your Geoguessr accuracy.", 'buildings': "To identify buildings in Geoguessr, look for distinctive features such as the multi-storey gray stone structures of Andorra, Bermuda's bright colored houses with striking white roofs, Mexico's circular electricity meters and conspicuous black water tanks, Greenland's colorful homes, Switzerland's penchant for window shutters and wooden constructions, Rwanda's property-surrounding high walls, uniquely structured bus stop shelters in Chile, vertically-columned Malaysian houses, Dubai's towering skyscrapers, Bhutan's elaborate homes with extended flat roofs, Curaçao's vividly colored architecture, Cambodia's elevated homes, Pakistan's proximity to religious monuments, and the traditional round thatched huts of Lesotho. Each of these traits is reflective of the local styles and can be key to pinpointing your virtual location.", 'flora': "Recognizing flora in Geoguessr can be pivotal for pinpointing your virtual location. For instance, the sight of Eucalyptus trees with white bark can lead you straight to Australia, while a lack of trees and presence of tabletop mountains could suggest you're in Lesotho. Encountering tall mountains and verdant hills might mean you're in Bhutan or Switzerland, and tropical landscapes with abundant palm trees likely indicate you're somewhere like Sri Lanka or Thailand. Painted tree trunks are a visual hint of being in Ukraine, and if you find yourself surrounded by unique cabbage-like vegetation, chances are you've landed in Japan's northern areas. On the other hand, flat roads with a backdrop of volcanic activity and mountains might mean Iceland, unless you're viewing verdant hills and fewer trees, which could point to Norway. Navigating these natural cues will significantly enhance your Geoguessr gameplay.", 'guardrails': "Recognizing the right guardrails can significantly improve your geo-deduction skills in Geoguessr. Lithuania's guardrails stand out with unique orange reflectors, as opposed to Latvia's red and white ones and Estonia's lack of reflectors entirely. Spotting a type B guardrail that's wider in the middle could point you toward Czechia or Slovakia. Meanwhile, Ecuador might reveal itself by its frequent use of double guardrails—a rarity in South America. Remembering these guardrail features can be a game-changer in identifying your location.", 'chevrons': 'Recognizing locations in Geoguessr can be enhanced by understanding chevrons – arrow-like road markings often used for indicating curves, roundabouts or traffic islands. In different countries, these patterns vary in color, size, and frequency. Spotting distinct chevron styles can hint at specific regions: large bright yellow chevrons might suggest North American roads, while smaller white ones could point towards European countries. Always consider road texture and surrounding signage, as these complement the chevron clues and improve your geographic deduction skills.', 'milestones': "Milestone markers are crucial clues in Geoguessr for pinpointing your location on the map. They vary widely, from the Michelin-style bornes in France to the distinctively shaped Meilensteine in Germany. In the US, look for the small reference markers along highways, uniquely numbered to each state's system. In many countries, these markers will often include numbers indicating distance to the nearest towns or the road number, which you can cross-reference with the map. Recognizing the language on the sign can highly narrow down the region—Kilometer markers in Russia, for example, use Cyrillic script, immediately pointing to a post-Soviet country. Keep an eye on the design and language of milestone markers—they can be a direct line to your virtual location.", 'signposts': "When playing Geoguessr, recognizing sign posts can hugely boost your location-deducing skills. Look for language clues, which can often reveal the country or even the region. Alphabets like Cyrillic or scripts like Thai are dead giveaways. Pay attention to the color and shape of road signs—many countries have unique designs. Traffic direction hints at whether you're in a right-hand or left-hand drive country. Distinctive landscapes or city names on signposts can also narrow down the search. Always consider sign wear and tear; it may suggest weather patterns typical of the region."}


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
            log.info(f"Category {input_category[1]} created")
    
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
            log.info(f"Quiz {quiz_name} created")
        
        # Add Quiz FK to Category
        category.quiz = quiz_db
        category.save()


    # Region Quizzes
    regions = Region.objects.all()
    for region in regions:
        # Name
        quiz_name = region.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)  
            log.info(f"Quiz {quiz_name} created")
        
        # Set all countries in region
        countries = Country.objects.filter(region=region)
        quiz_db.countries.set(countries)
        
        # Add Quiz FK to Region
        region.quiz = quiz_db
        region.save()
    
    
    # Country Quizzes
    countries = Country.objects.all()
    for country in countries:
        # Name
        quiz_name = country.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
            log.info(f"Quiz {quiz_name} created")
        
        # Set country
        quiz_db.countries.set([country,])
        
        # Add Quiz FK to Country
        country.quiz = quiz_db
        country.save()
    
    
    # Create 'Random' quiz for all facts
    random_quiz_name = Quiz.RANDOM_QUIZ_NAME
    try:
        quiz_db = Quiz.objects.get(name=random_quiz_name)
    except Quiz.DoesNotExist:
        quiz_db = Quiz.objects.create(name=random_quiz_name)
        log.info(f"Quiz {random_quiz_name} created")
    
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        
        # Delete quiz if no facts
        quiz = Quiz.objects.get(uuid=quiz.uuid)
        if quiz.num_facts == 0:
            quiz.delete()
            log.info(f"Quiz {quiz.name} deleted")
    
        