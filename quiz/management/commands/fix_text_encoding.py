from django.core.management.base import BaseCommand
from quiz.models import Fact

class Command(BaseCommand):
    help = 'Fix text encoding issues in facts'

    def handle(self, *args, **options):
        def fix_text(text):
            if not text:
                return text
            
            replacements = {
                'â€™': "'",     # right single quotation mark
                'â€œ': '"',     # left double quotation mark  
                'â€': '"',      # right double quotation mark
                'â€"': '—',     # em dash
                'â€"': '–',     # en dash
                'Ã¤': 'ä',     # a with umlaut
                'Ã¼': 'ü',     # u with umlaut
                'Ã¶': 'ö',     # o with umlaut
                'ÃŸ': 'ß',     # sharp s
                'Ã„': 'Ä',     # A with umlaut
                'Ãœ': 'Ü',     # U with umlaut
                'Ã–': 'Ö',     # O with umlaut
            }
            
            fixed_text = text
            for broken, correct in replacements.items():
                fixed_text = fixed_text.replace(broken, correct)
            
            return fixed_text

        facts = Fact.objects.all()
        fixed_count = 0

        for fact in facts:
            original_answer = fact.answer
            original_notes = fact.notes
            
            fixed_answer = fix_text(original_answer)
            fixed_notes = fix_text(original_notes) if original_notes else None
            
            if fixed_answer != original_answer or fixed_notes != original_notes:
                fact.answer = fixed_answer
                fact.notes = fixed_notes
                fact.save()
                fixed_count += 1
                self.stdout.write(f"Fixed fact {fact.uuid}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} facts')
        )