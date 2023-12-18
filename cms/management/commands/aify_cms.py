from django.core.management.base import BaseCommand
from django.conf import settings
from openai import OpenAI
import logging
log = logging.getLogger(__name__)

from .ai_input.prompt import SYSTEM_MESSAGE, USER_MESSAGE

# https://platform.openai.com/docs/models
# https://openai.com/pricing
OPEN_AI_MODEL = "gpt-4-1106-preview"


class Command(BaseCommand):

    def handle(self, *args, **options):
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        completion = client.chat.completions.create(
            model=OPEN_AI_MODEL,
            messages=[
                {"role": "user", "content": SYSTEM_MESSAGE.strip()},
                {"role": "user", "content": USER_MESSAGE.strip()}
            ]
        )

        print("********** COMPLETION **********")
        print(completion.choices[0].message.content)
        print("**********    INFO    **********")
        print("prompt_tokens: %s" % completion.usage.prompt_tokens)
        print("completion_tokens: %s" % completion.usage.completion_tokens)
        print("total_tokens: %s" % completion.usage.total_tokens)
        price_usd = completion.usage.total_tokens * 0.01 / 1000
        print("price: $%s" % round(price_usd, 4))
        print("requests per $1: %s" % int((1/price_usd)))
        print("**********    DONE    **********")
