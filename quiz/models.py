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
    

class Facts(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.CharField(max_length=250)
    difficulty = models.IntegerField()
    question_type = models.CharField(max_length=250)
    notes = models.CharField(max_length=250)
    google_streetview_url = models.CharField(max_length=250)
    airtable_id = models.CharField(max_length=100)

    def __str__(self):
        return self.question[:50] if self.question else 'No question'