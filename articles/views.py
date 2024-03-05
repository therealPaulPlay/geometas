from django.shortcuts import render
import copy

from quiz.models import Country, Fact


def country_coverage(request):
    country_count = Country.objects.count()
    context = {
        'countries': Country.objects.all().order_by('region__sort_order', 'name').select_related('quiz', 'region__quiz'),
        'country_count': country_count,
        'html_meta_title': "Geoguessr Country Coverage",
        'html_meta_description': "In Geoguessr you can encounter up to %s countries. Learn the Geoguessr metas for each country to become a Geoguessr champion." % country_count,
        'html_meta_image_url': request.build_absolute_uri('/static/seo/country_coverage.png'),
    }
    return render(request, 'articles/country_coverage.html', context)


def driving_direction(request):
    context = {
        'countries': Country.objects.all().order_by('name').select_related('quiz'),
        'html_meta_title': "Driving direction in Geoguessr",
        'html_meta_description': "The direction of traffic is a key meta in Geoguessr. Learn the driving direction for each country to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/driving_direction.png'),
    }
    return render(request, 'articles/driving_direction.html', context)


def eastern_europe(request):
    languages = {
        "latin": Fact.objects.get(airtable_id="recqNCngQR2DXrjfz"),
        "both": Fact.objects.get(airtable_id="recS1GDw2ihg83uQv"),
        "cyrillic": Fact.objects.get(airtable_id="recRKCFfddnmnFV0U"),
    }
    bollard = {
        "hungary": Fact.objects.filter(category__slug="bollards", country__slug="hungary").first(),
        "slovenia": Fact.objects.filter(category__slug="bollards", country__slug="slovenia").first(),
        "slovakia": Fact.objects.filter(category__slug="bollards", country__slug="slovakia").first(),
    }
    warning_sign = Fact.objects.get(airtable_id="recAhLi7tmiRgab9K")
    directional_signs = {
        "green": Fact.objects.get(airtable_id="recrti8CSFCOOQhHX"),
        "yellow": Fact.objects.get(airtable_id="rec3PWgpmNOrrVPPC"),
        "blue": Fact.objects.get(airtable_id="recDjo4Syy89o6KaO"),
    }
    uniques = {
        "rift": Fact.objects.get(airtable_id="recXrWdj97x8taiOJ"),
        "holey_pole": Fact.objects.get(airtable_id="recL1IehAsZgyVXTV"),
        "albania_license_plate": Fact.objects.get(airtable_id="receyxRDqnI6yxVtu"),
        "ukraine_google_car": Fact.objects.get(airtable_id="rectcLmHQY0fnPnHW"),
        "no_antenna": Fact.objects.get(airtable_id="recKDzh6pC6co9gkm"),
        "hungary_road_marker": Fact.objects.get(airtable_id="recAmDvHOIO0TRSyt"),
        "romania_road_marker": Fact.objects.get(airtable_id="recAcphJ7gaoJUrVd"),
        "slovenia_road_marker": Fact.objects.get(airtable_id="recSAQvo4pRfOP7EX"),
        "romania_yellow_sign": Fact.objects.get(airtable_id="recNRvyTTPazZ12yn"),
        "white_trees": Fact.objects.get(airtable_id="recXkaRoxe8URAuZF"),
        "bulgaria_poles": Fact.objects.get(airtable_id="recI20n5tP82U3zt8"),
        "hungary_hydrant": Fact.objects.get(airtable_id="recLF9YHiUxOB0gml"),
        "croatia_hydrant": Fact.objects.get(airtable_id="recvrPtJKoclKERj6"),
    }
    
    context = {
        'languages': languages,
        'bollards': bollard,
        'warning_signs': warning_sign,
        'directional_signs': directional_signs,
        'uniques': uniques,
        'html_meta_title': "Country-guessing Eastern Europe",
        'html_meta_description': "Eastern Europe is a region in Geoguessr. Learn the countries in Eastern Europe to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/eastern_europe.png'),
    }
    return render(request, 'articles/eastern_europe.html', context)


def world_map_common_locations(request):
    facts = {
        "hong_kong": Fact.objects.get(airtable_id="recLhAiKhFfBcV4Sd"),
        "midway_atoll": Fact.objects.get(airtable_id="recUgzOC1LIFgzlrS"),
        "xmas_island": Fact.objects.get(airtable_id="recmvCVQEvgwq30sv"),
        "bermuda": Fact.objects.get(airtable_id="receGLe5opxKOJCRy"),
        "madagascar_boat": Fact.objects.get(airtable_id="recYZ7O6Qk1fQMktB"),
        "madagascar_trekker": Fact.objects.get(airtable_id="recyK6OYPOPzEoCUG"),
        "monaco": Fact.objects.get(airtable_id="recvxUK4ni7oIoMnI"),
        "vienna": Fact.objects.get(airtable_id="rec8iDOvUqIaHLkMo"),
        "singapore": Fact.objects.get(airtable_id="rec9hEYcOwW90WHcq")
    }
    context = {
        'facts': facts,
        'html_meta_title': "The Most Common Geoguessr World Map Locations",
        'html_meta_description': "Find the most common locations on the Geoguessr world map to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/world_map.jpg'),
    }
    return render(request, 'articles/world_map_common_locations.html', context)


def south_african_countries(request):
    facts = {
        "landscape": {
            "za": Fact.objects.get(airtable_id="reczOidbaTUzO1STa"),
            "bw": Fact.objects.get(airtable_id="recOFlH3oYGnbwAws"),
            "ls": Fact.objects.get(airtable_id="recmSErrRkPVTu3WF"),
            "sz": Fact.objects.get(airtable_id="recJuSsPub8EBpjrC"),
        },
        "road_names": {
            "za": Fact.objects.get(airtable_id="recsocCI1w2pgB7xb"),
            "bw": Fact.objects.get(airtable_id="recWdVZrnHBuc1akc"),
            "ls": Fact.objects.get(airtable_id="recSV2CDdndB21Qcb"),
            "sz": Fact.objects.get(airtable_id="rec5e3S51TI8eNvVK"),
        },
        "uniques": {
            "za_chevrons": Fact.objects.get(airtable_id="recL0VdwPgEBf9gaL"),
            "za_gen2": Fact.objects.get(airtable_id="recWdqg8xB95fg2Pt"),
            "ls_blanket": Fact.objects.get(airtable_id="recm47pOVclnJu7AP"),
            "ls_huts": Fact.objects.get(airtable_id="reci9yiBkW0F8uJH3"),
            "bw_signpost": Fact.objects.get(airtable_id="recMVDmrhwxvgB2Rz"),
            "sz_poles": Fact.objects.get(airtable_id="recmM2AGUQirOTqqJ"), 
        }
    }
    context = {
        'facts': facts,
        'html_meta_title': "Country-guessing Southern Africa",
        'html_meta_description': "Learn the most relevant Geoguessr metas to identify South Africa, Botswana, Eswatini, and Lesotho.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/south_africa.png'),
    }
    return render(request, 'articles/south_african_countries.html', context)



def latin_america(request):
    facts = {
        "easy": {
            "br_lang": Fact.objects.get(airtable_id="recKlE0T6Bgf0PAQk"),
            "black_car": Fact.objects.get(airtable_id="recegeaejCsi778fX"),
            "uy_overcast": Fact.objects.get(airtable_id="recunqjCGpJNIY4wS"),
            "mx_stop": Fact.objects.get(airtable_id="recmrUL5xw4uu6NbM"),
        },
        "license_plates": {
            "br": Fact.objects.get(airtable_id="recawRpccIfzUD1gp"),
            "ar": Fact.objects.get(airtable_id="reckdFHzAaJmc7SUT"),
            "co": Fact.objects.get(airtable_id="rec612bmiWMRv3C4j"),
            "ec": Fact.objects.get(airtable_id="recJG7srWhqXkjIWz"),
        },
        "milestones": {
            "br": Fact.objects.get(airtable_id="recff0Ik4skDcyhj5"),
            "ar": Fact.objects.get(airtable_id="recyDxGHvGK44IAUi"),
            "uy": Fact.objects.get(airtable_id="recByR3K4qCIMkmiV"),
            "cl": Fact.objects.get(airtable_id="recbtPqqSbnemFAsq"),
            "co": Fact.objects.get(airtable_id="receUwMRY1nheW5kU"),
        },
        "signposts": {
            "br": Fact.objects.get(airtable_id="recWQah3rdoEIfUJJ"),
            "uy": Fact.objects.get(airtable_id="recQft8BR0F6339Qu"),
            "co": Fact.objects.get(airtable_id="recpgrBny8VSFzdPb"),
            "ec": Fact.objects.get(airtable_id="recNAWFDClJPBBMJL"),
            "uy": Fact.objects.get(airtable_id="recQft8BR0F6339Qu"),
            "cl": Fact.objects.get(airtable_id="rec1x9f30oEDouC6b"),
            "bo": Fact.objects.get(airtable_id="recQq3hvgei9IGRdl"),
            "pe": Fact.objects.get(airtable_id="recNrZMPUBQqYB7Ue"), 
        },
        "poles": {
            "br": Fact.objects.get(airtable_id="recYT9xm6HXILql3C"),
            "ar": Fact.objects.get(airtable_id="recLr5Qwya4xYjaVM"),
            "uy": Fact.objects.get(airtable_id="recbSqcA91CLCuzYf"),
            "co": Fact.objects.get(airtable_id="reclFOvy6E3775hP4"),
            "ec": Fact.objects.get(airtable_id="recJN8eV0GsNze6f6"),
            "cl": Fact.objects.get(airtable_id="recWb2PakDetVCNv0"),
            "mx_co": Fact.objects.get(airtable_id="recOS5xEzGhLFQjyi"),
            "pe": Fact.objects.get(airtable_id="recIlL6wXQftTnnQP"),
        },
        "road_markings": {
            "br": Fact.objects.get(airtable_id="recx9eHtJ9GcgEeE6"),
            "ar_uy": Fact.objects.get(airtable_id="recQ4HItudYHVo6ZI"),
            "uy": Fact.objects.get(airtable_id="recpArdpHwIpfVxn7"),
            "cl": Fact.objects.get(airtable_id="rec3BZ4znZPlTNyS0"),
        },
        "uniques":{
            "br_chevron": Fact.objects.get(airtable_id="recSeCzJqjBfTjykf"),
            "br_dishes": Fact.objects.get(airtable_id="recE2KCQrNLsbDuN7"),
            "ar_chevron": Fact.objects.get(airtable_id="recaTnH59sa3DVLwz"),
            "uy_arrows": Fact.objects.get(airtable_id="rec5ZlY6VDpX4zkeQ"),
            "uy_trafficlights": Fact.objects.get(airtable_id="recXPIuAw90ulQPGo"),
            "cl_google_car": Fact.objects.get(airtable_id="rec2PfXhfJT7CtD80"),
            "cl_bus_stop": Fact.objects.get(airtable_id="rec1V9N7Bu1wE1bma"),
            "ec_bollards": Fact.objects.get(airtable_id="recQ67VX5WIZkGZJK"),
            "ec_double_guardrail": Fact.objects.get(airtable_id="reca7qmUn0BmtWE8z"),
            "co_taxis": Fact.objects.get(airtable_id="rec33UwISuPwDckxN"),
            "co_fence": Fact.objects.get(airtable_id="recCJ6As5Uv9TWVXm"),
            "co_sidewalk": Fact.objects.get(airtable_id="recQXzZU6Yb1j6EXG"),
            "pe_counter": Fact.objects.get(airtable_id="reclO1QGQHEPCqR5B"), 
            "pe_rikshaw": Fact.objects.get(airtable_id="recbKD4hGMSmQrs8Z"), 
            "mx_counter": Fact.objects.get(airtable_id="recCVBKrzKxpYM833"),
            "mx_tank": Fact.objects.get(airtable_id="rece3lzUqO6xeBdso"),
        }
    }
    context = {
        'facts': facts,
        'html_meta_title': "Country-guessing Latin America",
        'html_meta_description': "Learn the most relevant Geoguessr metas to identify the main Latin American countries: Brazil, Argentina, Mexico, Peru, Uruguay, Ecuador, Colombia, Bolivia, and Chile.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/latin_america.png'),
    }
    return render(request, 'articles/latin_america.html', context)


def nordics(request):
    facts = {
        "isfo": {
            "is_landscape": Fact.objects.get(airtable_id="recbTF8Fyif1Fwc1a"),
            "is_bollard": Fact.objects.get(airtable_id="recZjUf6lFJKJDHsM"),
            "fo_landscape": Fact.objects.get(airtable_id="recVHlQ0IvQiPuAAO"),
            "fo_car": Fact.objects.get(airtable_id="recKgmcmtCvRMXVCk"),
        },
        "road_markings": {
            "dk": Fact.objects.get(airtable_id="recdKb67HYla0jhix"),
            "no": Fact.objects.get(airtable_id="recnWBxGeY9ELtPGY"),
            "se": Fact.objects.get(airtable_id="reccKxIzYIjYl2Vyk"),
            "fi": Fact.objects.get(airtable_id="recthzUZz6lTVxyGU"),
        },
        "giveway_sign": {
            "dk": Fact.objects.get(airtable_id="recGX3NfgsRN81BdY"),
            "no": Fact.objects.get(airtable_id="recKBmtGYIoctGDU4"),
            "se": Fact.objects.get(airtable_id="rectvlwuA7NB7MHLk"),
            "fi": Fact.objects.get(airtable_id="recXGQjVGBVaKHEZW"),
        },
        "language": {
            "dk": Fact.objects.get(airtable_id="recvpr0t4XFbN6CuX"),
            "no": Fact.objects.get(airtable_id="recVpOYNf9wYBukxs"),
            "se": Fact.objects.get(airtable_id="recc9H7izDidSzGkO"),
            "fi": Fact.objects.get(airtable_id="rectq62OjHhiQbDyj"),
            "is": Fact.objects.get(airtable_id="recVEuKE9w1wPyaBn"),
        },
        "bollards": {
            "dk": Fact.objects.get(airtable_id="recdaFxNHMs9woKrU"),
            "se": Fact.objects.get(airtable_id="recNG5egXPIMuavOu"),
            "fi": Fact.objects.get(airtable_id="rec8a7mHYz4B0tJwv"),
            "is": Fact.objects.get(airtable_id="recZjUf6lFJKJDHsM"),
        },
        "direction_sign": {
            "dk": Fact.objects.get(airtable_id="recctMSnmyCCajGgC"),
            "no": Fact.objects.get(airtable_id="recml8WZQjWYqs9LK"),
            "se": Fact.objects.get(airtable_id="recymdJQGucwb4Q3n"),
            "fi": Fact.objects.get(airtable_id="recZU6fCDtoQfwLoK"),
        },
        "uniques":{
            "no_green": Fact.objects.get(airtable_id="reclQeees8dbRYxPA"),
            "dk_yellow": Fact.objects.get(airtable_id="recFrzGj34PIaRj1r"),
            "se_chevron": Fact.objects.get(airtable_id="recLmwVRP19x3ADCj"),
            "fi_dirtroad": Fact.objects.get(airtable_id="reckfmejpFMLOa9yg"),
            "is_pedyellow": Fact.objects.get(airtable_id="recJ3SiekYDIGxFcZ"),
        }
    }
    context = {
        'facts': facts,
        'html_meta_title': "Country-guessing Europe's Nordic Countries",
        'html_meta_description': "Learn the most relevant Geoguessr metas to identify the Nordic countries in Europe: Norway, Sweden, Finland, Denmark, Iceland, and the Faroe Islands.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/nordics.png'),
    }
    return render(request, 'articles/nordics.html', context)


def australia_new_zealand(request):
    facts = {
        "bollards": {
            "au": Fact.objects.get(airtable_id="recadtEFirgLEBMzp"),
            "nz": Fact.objects.get(airtable_id="recvoX8oU3zL9YwtO"),
        },
        "giveway": {
            "au": Fact.objects.get(airtable_id="recWXamEMlek9YMu1"),
            "nz": Fact.objects.get(airtable_id="recuCIJ9BfSYEVCkN"),
        },
        "speed": {
            "au": Fact.objects.get(airtable_id="reclTHsJTSmdBV9hO"),
            "nz": Fact.objects.get(airtable_id="reckHK6z7edNFpXLN"),
        },
        "street": {
            "au": Fact.objects.get(airtable_id="recsMFil4wE5NIFUP"),
            "nz": Fact.objects.get(airtable_id="recjgR4m8RN8LfOMW"),
        },
        "chevron": {
            "au": Fact.objects.get(airtable_id="recjn9gWerSHM5OAv"),
            "nz": Fact.objects.get(airtable_id="recpiYU68FXMuNhTU"),
        },
        "flora": {
            "au": Fact.objects.get(airtable_id="recuY1l9FbKAgojX0"),
            "nz": Fact.objects.get(airtable_id="recOcGuAZczLfB7we"),
        },
        "others": {
            "nz_giveway": Fact.objects.get(airtable_id="recDnOYYTZ8sI60Np"),
            "nz_wrap": Fact.objects.get(airtable_id="recuboFUD4ePyguWF"),
        }
    }
    context = {
        'facts': facts,
        'html_meta_title': "Country-guessing Australia vs. New Zealand",
        'html_meta_description': "Learn the most relevant Geoguessr metas to tell Australia apart from New Zealand.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/australia_new_zealand.png'),
    }
    return render(request, 'articles/australia_new_zealand.html', context)


def south_east_asia(request):
    facts = {
        "license_plates": {
            "yellow": Fact.objects.get(airtable_id="recc75037uI4rJYV6"),
            "black_malay": Fact.objects.get(airtable_id="recpYqx87zFyIp7lm"),
            "black_indo": Fact.objects.get(airtable_id="recdewQ75Xy0H99QP"),
            "phili": Fact.objects.get(airtable_id="rec4cMmGAg7YZhqYx"),
        },
        "signposts": {
            "thai": Fact.objects.get(airtable_id="recT0BV8HYAC6SLc5"),
            "stripes": Fact.objects.get(airtable_id="recMNg9xFKSJyj1Ny"),
        },
        "poles": {
            "thai_holes": Fact.objects.get(airtable_id="rect2AIau42lYOM2A"),
            "thai_base": Fact.objects.get(airtable_id="recNXaFIXRuvC8BYF"),
            "malay": Fact.objects.get(airtable_id="recp7OgJbHd9esnHV"),
            "indo": Fact.objects.get(airtable_id="reclcY3by0A8EsSyE"),
            "sri_1": Fact.objects.get(airtable_id="recMp7XQEGUnETtTy"),
            "sri_2": Fact.objects.get(airtable_id="recPdT1aqfphiJW58"),
            "cambo_1": Fact.objects.get(airtable_id="recdFiozuQF8YO9UQ"),
            "cambo_2": Fact.objects.get(airtable_id="recu8htmlGJPdx5KH"),
        },
        "street_markings": {
            "yellow": Fact.objects.get(airtable_id="reccQvQPhPHEegZGy"),
            "white": Fact.objects.get(airtable_id="recrht9uCi0FtXB1g"),
        },
        "bollards": {
            "thai": Fact.objects.get(airtable_id="rect9bMNIiOpXIciK"),
            "malay_1": Fact.objects.get(airtable_id="recjh73BZi3f9XE2I"),
            "malay_2": Fact.objects.get(airtable_id="recl4w0TB3S8tYdfZ"),
            "cambo": Fact.objects.get(airtable_id="recfPLlvDkNs2n0Bx"),
            "sri": Fact.objects.get(airtable_id="recb2rBbzp7VkEvZK"),
        },
        "language": {
            "thai": Fact.objects.get(airtable_id="recjDJO2LcjNFeU64"),
            "cambo": Fact.objects.get(airtable_id="recPwhXJyDTSGPW0U"),
            "sri": Fact.objects.get(airtable_id="rec0St1RDzaSFZQ0U"),
            "indo_malay": Fact.objects.get(airtable_id="recWdKYhB1l08Zpnx"),
        },
        "other": {
            "indo_dish": Fact.objects.get(airtable_id="rec2BHJKKAcPbrMvt"),
            "malay_bars": Fact.objects.get(airtable_id="rec1CfzEikASdNM4z"),
            "malay_stop": Fact.objects.get(airtable_id="recgQOl3kDkul9k9D"),
            "phili_sidecar": Fact.objects.get(airtable_id="reclQydq3wIjWO6m7"),
            "phili_roads": Fact.objects.get(airtable_id="recJ13mIV3HqXJXsb"),
            "phili_bus": Fact.objects.get(airtable_id="recOsooCA6LW660dc"),
            "sri_googlecar": Fact.objects.get(airtable_id="recEcTUKlov1fzhs5"),
            "sri_lowcam": Fact.objects.get(airtable_id="rec2jX0WS27uKDBy6"),
            "sri_soil": Fact.objects.get(airtable_id="recJNy9Vw1VctVkfN"),
            "cambo_beer": Fact.objects.get(airtable_id="recFaefWPn00C1ytO"),
            "cambo_houses": Fact.objects.get(airtable_id="rec3uIzFShQEWIvqA"),
        }
    }
    context = {
        'facts': facts,
        'html_meta_title': "Country-guessing South-East Asia",
        'html_meta_description': "Learn the most relevant Geoguessr metas to identify the South-East Asian countries Thailand, Malaysia, Indonesia, Philippines, Cambodia, and Sri Lanka.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/south_east_asia.png'),
    }
    return render(request, 'articles/south_east_asia.html', context)