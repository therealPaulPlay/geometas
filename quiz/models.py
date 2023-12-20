from django.db import models
import uuid
import logging
log = logging.getLogger(__name__)


class Region(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Regions"


class Country(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    iso2 = models.CharField(max_length=2)
    continent = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='countries', null=True)

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


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Fact(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    countries = models.ManyToManyField(Country, related_name='facts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='facts', null=True)
    difficulty = models.IntegerField()
    notes = models.CharField(max_length=1000, null=True, blank=True)
    google_streetview_url = models.CharField(max_length=250, null=True, blank=True)
    airtable_id = models.CharField(max_length=100)
    distinctive = models.BooleanField(default=False, null=True, blank=True)
    distinctive_in_region = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.answer[:50] + (self.answer[50:] and '...')
    

class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    countries = models.ManyToManyField(Country, related_name='quizzes', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
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