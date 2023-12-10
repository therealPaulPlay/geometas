from django.db import models
import uuid


class Country(models.Model):
    name = models.CharField(max_length=250)
    iso2 = models.CharField(max_length=2)
    continent = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'iso2')
        verbose_name_plural = "Countries"
    

class Fact(models.Model):
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
        ("pedestrian_crossign_sign", "Pedestrian Crossign Sign"),
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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
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
    