from django.db import models
import uuid
import logging
log = logging.getLogger(__name__)


CATEGORY_CHOICES = [
    ("coverage", "Coverage"),
    ("driving_direction", "Driving direction"),
    ("google_car", "Google Car"),
    ("language", "Language"),
    ("license_plate", "License Plate"),
    ("road_lines", "Road Lines"),
    ("settlement_sign", "Settlement Sign"),
    ("bollards", "Bollards"),
    ("street_numbering", "Street Numbering"),
    ("street_markings", "Street Markings"),
    ("street_name", "Street Name"),
    ("street_sign", "Street Sign"),
    ("poles", "Poles"),
    ("other", "Other"),
    ("cars", "Cars"),
    ("pedestrian_crossign_sign", "Pedestrian Crossing Sign"),
    ("buildings", "Buildings"),
    ("flora", "Flora"),
]

QUESTION_TYPE_CHOICES = [
    ("SingleCountry", "SingleCountry"),
    ("SingleContinent", "SingleContinent"),
    ("MultipleCountry", "MultipleCountry"),
    ("MultipleContinent", "MultipleContinent"),
    ("NoAnswer", "NoAnswer"),
]


class Country(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    iso2 = models.CharField(max_length=2)
    continent = models.CharField(max_length=200)
    region = models.CharField(max_length=200, null=True, blank=True)
    region_slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def flag_emoji(self):
        # Make sure the country code is in uppercase
        iso2 = self.iso2.upper()
        # Convert each letter to the corresponding regional indicator symbol
        return ''.join(chr(ord(letter) + 0x1F1A5) for letter in iso2)

    class Meta:
        unique_together = ('name', 'iso2')
        verbose_name_plural = "Countries"
    

class Fact(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    countries = models.ManyToManyField(Country, related_name='facts')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    difficulty = models.IntegerField()
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPE_CHOICES)
    notes = models.CharField(max_length=1000, null=True, blank=True)
    google_streetview_url = models.CharField(max_length=250, null=True, blank=True)
    airtable_id = models.CharField(max_length=100)

    def __str__(self):
        return self.answer[:50] + (self.answer[50:] and '...')

    @property
    def question(self):
        return {
            "SingleCountry": "Which country is this?",
            "MultipleCountry": "Which countries are these?",
            "SingleContinent": "Which continent is this?",
            "MultipleContinent": "Which continents are these?",
            "NoAnswer": "General learning: did you know this?"
        }[self.question_type]
    

class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    countries = models.ManyToManyField(Country, related_name='quizzes', blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_facts = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('name',)
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.name[:50] + (self.name[50:] and '...')

    def get_facts(self):
        # Retrieve all facts, will have dupes due to M2M relationship
        facts = Fact.objects.all()
        if self.category:
            facts = facts.filter(category=self.category)
        if self.countries and self.countries.count() > 0:
            facts = facts.filter(countries__in=self.countries.all())
        
        # Getting distinct primary keys
        fact_ids = facts.values_list('uuid', flat=True).distinct()
        
        # Querying Fact objects based on the distinct ids
        return Fact.objects.filter(uuid__in=fact_ids).order_by('?')
    
    def update_num_facts(self):
        self.num_facts = self.get_facts().count()
        self.save()
        log.info(f"Quiz {self.name} updated with {self.num_facts} facts")


class QuizSession(models.Model):
    SESSION_STATES = [
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
        ("cancelled", "Cancelled"),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=SESSION_STATES, default="in_progress")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'state'],
                condition=models.Q(state='in_progress'),
                name='unique_user_in_progress'
            )
        ]
        verbose_name_plural = "Quiz Sessions"

    def __str__(self):
        return f"{self.uuid} - {self.user.username} - {self.quiz.name} - {self.state}"
    
    def load_facts(self):
        # Get facts
        facts = self.quiz.get_facts()
        
        # Iterate over facts to create QuizSessionFact objects with sort_order
        index = 1
        for fact in facts:
            QuizSessionFact.objects.create(
                user=self.user,
                quiz=self.quiz,
                quiz_session=self,
                fact=fact,
                sort_order=index
            )
            index += 1

        log.info(f"Loaded {facts.count()} facts for {self.quiz.name} quiz session")



class QuizSessionFact(models.Model):
    REVIEW_RESULT = [
        ("correct", "Correct"),
        ("false", "False"),
        ("not_set", "Not Set"),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='quizsessionfacts')
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    sort_order = models.IntegerField()
    review_result = models.CharField(max_length=100, choices=REVIEW_RESULT, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_session} - {self.fact}"

    class Meta:
        unique_together = ('quiz_session', 'fact')
        verbose_name_plural = "Quiz Session Facts"