from django.db import models
import uuid
import math
import logging
log = logging.getLogger(__name__)


class Region(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    quiz = models.OneToOneField('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True, related_name='region_quiz')

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
    quiz = models.OneToOneField('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True, related_name='country_quiz')
    right_hand_traffic = models.BooleanField(default=True)

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
    quiz = models.OneToOneField('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True, related_name='category_quiz')

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
    notes = models.CharField(max_length=1000, null=True, blank=True)
    google_streetview_url = models.CharField(max_length=250, null=True, blank=True)
    airtable_id = models.CharField(max_length=100)
    distinctive = models.BooleanField(default=False, null=True, blank=True)
    distinctive_in_region = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.answer[:50] + (self.answer[50:] and '...')

    def get_question(self):
        if not self.distinctive:
            return "Which country(s) in %s is this?" % self.countries.first().region.name
        return "Which country(s) is this?"
    

class Quiz(models.Model):
    QUIZ_NUM_FACTS = 7
    RANDOM_QUIZ_NAME = "Random"
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
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
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
        return f"{self.uuid}"
    
    @property
    def num_questions(self):
        return Quiz.QUIZ_NUM_FACTS

    def mark_cancelled(self):
        self.state = "cancelled"
        self.save()
        log.info(f"Quiz session {self.uuid} marked as cancelled")
    
    def load_facts(self):
        # Get facts (in random order)
        facts = self.quiz.get_facts()
        
        # Add performance-based weighting if user is logged in
        if self.user:
            # Weigh facts based on user performance
            facts = self.weigh_facts_based_on_user_performance(facts)
        
        # Restrict to N facts 
        facts = facts[:Quiz.QUIZ_NUM_FACTS]
            
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

        log.info(f"Quiz session {self.uuid}: Loaded {len(facts)} facts for {self.quiz.name} quiz session")
        return facts

    def weigh_facts_based_on_user_performance(self, facts):
        # Prioritized fact_list
        performance_based_fact_list = []
        
        # First fill up with as many new facts as we have
        ufps = UserFactPerformance.objects.filter(user=self.user, fact__in=facts).exclude(box=0)
        
        # Box new facts
        facts_box_new = facts.exclude(userfactperformance__in=ufps)
        
        # Add all new facts to performance_based_fact_list
        performance_based_fact_list.extend(facts_box_new)
        from_box_new = len(facts_box_new)
        missing_fact_count = Quiz.QUIZ_NUM_FACTS - from_box_new
        
        # Add missing facts
        box_added_counts = {1: 0, 2: 0, 3: 0}
        if missing_fact_count > 0:
            # Box 1/2/3 facts
            facts_box_1 = ufps.filter(box=1)
            facts_box_2 = ufps.filter(box=2)
            facts_box_3 = ufps.filter(box=3)
            
            remaining_slots = 7 - len(performance_based_fact_list)
            box_1_needed = math.ceil(0.60 * remaining_slots)
            box_2_needed = math.ceil(0.14 * remaining_slots)
            box_3_needed = remaining_slots - box_1_needed - box_2_needed
            
            # Calculate how many elements to take from each box
            box_counts = {
                1: {"needed": box_1_needed, "available": facts_box_1.count()},
                2: {"needed": box_2_needed, "available": facts_box_2.count()},
                3: {"needed": box_3_needed, "available": facts_box_3.count()}  
            }
            gap = 0
            for box, count in box_counts.items():
                # If there are more available than needed, set gap to the difference
                if count["available"] < count["needed"]:
                    gap += count["needed"] - count["available"]
            
            # If there is a gap, take as many as possible from box 1, then box 2, then box 3
            if gap > 0:
                for box in range(1, 4):
                    # Calculate how many more this box has available
                    box_has_available = box_counts[box]["available"] - box_counts[box]["needed"]
                    # If this box has more available, take as many as possible up to the gap
                    if box_has_available > 0:
                        box_counts[box]["needed"] += min(box_has_available, gap)
                        gap -= min(box_has_available, gap)
                        if gap == 0:
                            break
            
            # Remove available key from dict and map to needed
            box_counts = {box: count["needed"] for box, count in box_counts.items()}

            # Add elements from each list
            for box, count in box_counts.items():
                if count > 0:
                    selected_facts = [ufp.fact for ufp in ufps.filter(box=box)[:count]]
                    performance_based_fact_list.extend(selected_facts)
                    # Add to box_added_counts
                    box_added_counts[box] = len(selected_facts)
            
        log.info(f"Quiz session %s fact distribution: New: {from_box_new}, Box 1: {box_added_counts[1]}, Box 2: {box_added_counts[2]}, Box 3: {box_added_counts[3]}")
        
        return performance_based_fact_list

    def get_next_fact(self):
        return QuizSessionFact.objects.filter(
            quiz=self.quiz,
            quiz_session=self,
            user=self.user,
            review_result__isnull=True
        ).order_by('sort_order').first()

    def mark_finished(self):
        self.state = "finished"
        self.save()
        log.info(f"Quiz session {self.uuid} marked as finished")
    

class QuizSessionFact(models.Model):
    REVIEW_RESULT = [
        ("correct", "Correct"),
        ("false", "False"),
        ("not_set", "Not Set"),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='quizsessionfacts')
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    sort_order = models.IntegerField()
    review_result = models.CharField(max_length=100, choices=REVIEW_RESULT, null=True, blank=True)
    
    class Meta:
        unique_together = ('quiz_session', 'fact')
        verbose_name_plural = "Quiz Session Facts"

    def __str__(self):
        return f"{self.user.username} - {self.quiz_session} - {self.fact}"
    
    def set_correct(self):
        # Set this session fact result to correct
        self.review_result = "correct"
        self.save()
        
        # Update UserFactPerformance if user is logged in
        if self.user:
            ufp = UserFactPerformance.objects.get_or_create(user=self.user, fact=self.fact)[0]
            ufp.set_correct()
    
    def set_false(self):
        # Set this session fact result to false
        self.review_result = "false"
        self.save()
        
        # Update UserFactPerformance if user is logged in
        if self.user:
            ufp = UserFactPerformance.objects.get_or_create(user=self.user, fact=self.fact)[0]
            ufp.set_false()
        



class UserFactPerformance(models.Model):
    MAX_BOX_NUM = 3
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    review_count = models.IntegerField(default=0)
    box = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'fact')
        verbose_name_plural = "User Fact Performances"
    
    def __str__(self):
        return f"{self.user.username} - {self.fact}"
    
    def set_correct(self):
        self.review_count += 1
        # Temp 0 fix
        if self.box == 0:
            self.box = 1
        if self.box < UserFactPerformance.MAX_BOX_NUM:
            self.box += 1
        self.save()
    
    def set_false(self):
        self.review_count += 1
        self.box = 1
        self.save()
    
    