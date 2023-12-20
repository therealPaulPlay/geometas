from django.core.management.base import BaseCommand
from django.conf import settings
from openai import OpenAI
import json
import logging
log = logging.getLogger(__name__)

from .ai_input.prompt import SYSTEM_MESSAGE
from quiz.models import Category, Region, Country, Fact

# https://platform.openai.com/docs/models
# https://openai.com/pricing
OPEN_AI_MODEL = "gpt-4-1106-preview"


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # Regions
        update_regions()

        # Categories
        update_categories()
        
        


def update_categories():
    categories = Category.objects.all()
    output_dict = {}
    for category in categories:
        
        # Create message
        user_message = create_user_message("Category: ", category.name, category.facts.all())

        # Call OpenAI
        completion = call_openai(SYSTEM_MESSAGE.strip(), user_message.strip())

        # Print output
        geo_content_output = completion.choices[0].message.content
        geo_content_output = geo_content_output.strip('```json\n ')
        geo_content_output = geo_content_output.strip('\n```')
        geo_content_output = json.loads(geo_content_output)['description']
        # print("**********   %s   **********" % category.name)
        # print(geo_content_output)
        # Add to output array
        output_dict[category.slug] = geo_content_output

    # Print output array
    print(output_dict)
    

def update_regions():
    regions = Region.objects.all()
    output_dict = {}
    for region in regions:
        
        # Get all Facts
        facts = []
        for country in region.countries.all():
            facts.extend(country.facts.all())
        facts = list(set(facts))
        
        # Create message
        user_message = create_user_message("Region: ", region.name, facts)

        # Call OpenAI
        completion = call_openai(SYSTEM_MESSAGE.strip(), user_message.strip())

        # Print output
        geo_content_output = completion.choices[0].message.content
        geo_content_output = geo_content_output.strip('```json\n ')
        geo_content_output = geo_content_output.strip('\n```')
        geo_content_output = json.loads(geo_content_output)['description']
        # print("**********   %s   **********" % region.name)
        # print(geo_content_output)
        # Add to output array
        output_dict[region.slug] = geo_content_output

    # Print output array
    print(output_dict)


def call_openai(system_message, user_message):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return client.chat.completions.create(
            model=OPEN_AI_MODEL,
            messages=[
                {"role": "user", "content": system_message},
                {"role": "user", "content": user_message.strip()}
            ]
        )


def create_user_message(type, name, facts):
    """
    Create the user message in this format:
    "<type>: <name>. <All fact.answer separated by ". ">"
    """
    # Get all questions
    questions = []
    for fact in facts:
        questions.append(fact.answer)
    
    # Create the message
    message = f"{type}: {name}. " + ". ".join(questions) + "."
    return message


#print("**********    INFO    **********")
#print("prompt_tokens: %s" % completion.usage.prompt_tokens)
#print("completion_tokens: %s" % completion.usage.completion_tokens)
#print("total_tokens: %s" % completion.usage.total_tokens)
#price_usd = completion.usage.total_tokens * 0.01 / 1000
#print("price: $%s" % round(price_usd, 4))
#print("requests per $1: %s" % int((1/price_usd)))
#print("**********    DONE    **********")