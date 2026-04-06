from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    demand_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class UnmatchedSearch(models.Model):
    term = models.CharField(max_length=255, unique=True)
    query_count = models.IntegerField(default=1)

    def __str__(self):
        return self.term
