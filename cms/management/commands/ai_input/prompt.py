# Multi-line system message to be imported in aify_cms.py
SYSTEM_MESSAGE = """
    You are creating website content for a website that helps Geoguessr users recognize locations based on country meta information ("metas"). 
    The user will share with you either a meta category, a broad geographical regiom, or a specific country name and you return the content. The goal of your content is to give the user the best chance to recognize the country they're in. 
    If the user shared a region or country, the goal of the content is to identify that region or country. If the user shared a category, the goal of the content is to describe how this category generally matters to identfy locations across the world.
    The content should generally enable the user to best recognize the country they see in Geoguessr via Google Streetview images. It should tell the user what's unique about the category, region, or country, which other regions or countries are similar, and how to recognize the category, region, or country best.
    The content should be informative and SEO-friendly and be in a casual tone. 
    The content should sound like a normal human writes. Use everyday, simple, straightforward, everyday words. Go straight into the content, no intros or salutations.
    Do not use many idioms, metaphors or figures ot speech.
    The content should be maxiumum 1000 characters.
    When the user gives you a category, the content should summarize the most important information. The content should not list individual country examples.
    The content should be returned as a JSON with two keys:
    "description": the content you wrote. max 1000 characters
    "data": show three keys nested within: "internet_domain", "iso2_code", "driving_direction", no other values. Only return this if a specific country name was given.

    The user will also give you some metas of the respective category, region, or country. Include the content of these metas if you consider them relevant for the user to recognize the country or region. 
"""

USER_MESSAGE = """ 
Category: Bollards

Metas: 
This is the front view of Hungarian, Bulgarian, Croatian and North Macedonian bollards. These countries also share the same white (rather than red, like the front) rectangle on the back of their bollards.

This is the main type of Serbian bollard. It resembles the bollards of Slovenia and Montenegro however the difference is that the Serbian red rectangle is always to one side- not in the centre.

These bollards are a common sight throughout Turkey and resemble the Australian and Netherlands bollards however they have a slightly fatter rectangle in Turkey.

The is a Czech and Slovakian bollard. Both Czech and Slovakian bollards have these unique fluro orange stripes in the black section of the bollard. The back of Czech and Slovakian bollards have a white rectangle in the black section.

This is the most common type of Ukrainian bollard. It has a red rectangle that is wider than the rectangles of Hungary, Bulgarian, Croatia and North Macedonia. Ukrainian bollards look like Russian bollards however Russian bollards are attached to a narrow support pole. Ukrainian bollards are typically run-down with the rectangle often damaged.

Polish bollards have a red diagonal stripe wrapping around the bollard.

The most common Italian bollard has a front that features a vertical, red rectangle inside a black, diagonal strip. Note that the black part goes to the top of the bollard- this is rare in the bollard world.

Finnish bollards are either cylindrical or look cylindrical from the front. This cylindrical shape isn’t shared by the bollards of the other Nordic countries.

The reflectors on the front of Austrian bollards are either blackish or dark red in colour. Seeing this black reflector and the black hat on the bollard is one of the easiest ways to tell that you are in Austria. No other countries have both of these features on their bollards.

These narrow, red and white signs are in some ways the bollard equivalent in South Africa. They are very common.

This is a Russian bollard. Russian bollards often have a unique feature- a narrow support pole on one side of them. This makes them unique from Ukrainian bollards. Russian bollards are primarily found at intersections.

Peru’s most common bollards look like cigarettes. They sometimes have the black stripes pictured here but on other occasions they lack these black stripes.

This is the front view of Slovenian and Montenegrin bollards.

Iceland has distinct yellow bollards with a top edge.

Ecuador has a number of different shaped bollards. The type pictured is the most common- featuring two red stripes. Another Ecuadorian bollard contains just one red stripe.

This is what the front of bollards in Denmark look like. They are a unique looking bollard and occur abundantly throughout the country. The rear of the bollard lacks the yellow section.

There are two types of French bollard, both are the same distinct shape and different from typical European bollard shapes. This is the first type with a gray reflector strip running around it. The second type has a red reflector strip.

Mexican bollards are white and cigarette shaped. They have a black section on the base of the bollard or near the base.

Cambodian bollards look a bit like fat matches. They have a white body and red head.

The front and back view of Japanese bollards.

Malaysian bollards have two red rectangles on them. Some bollards have two gray rectangles on one side.

Although bollards are relatively rare in the UK compared to some other European countries, they are rather unique looking and consist of black and white sections with a large red rectangle on top.

The most common type of Latvian bollard is a thin plank with a generic white rectangle on the front. The rear of the most common type of Latvian bollard has two white circles.

Standard Estonian bollards are cylindrical. This contrasts the narrow plank bollards of Lithuania and Latvia. The front of Estonian bollards have the white rectangle encased in the black section, similar to the Latvian bollards. Estonian bollards will on rare occasions have a yellow rectangle rather than the white rectangle. Estonian bollards have two white circles on their rear.

Thai bollards have an obelisk shape. They have alternating black and white sections

New Zealand has unique bollards lining their highways that have a red/orange strip that stretches around the higher part of the bollard.

Spanish feature the standard European black and white bollard with a bright yellow rectangle encased in the black section of the bollard.

This is what the front of Lithuanian bollards look like- they have a white rectangle on the rear instead of orange. These plastic bollards (that look like wood) with an orange rectangle are one of the best ways to distinguish Lithuania from the other Baltic countries (and other European countries).
"""