from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_fresher = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    experience_summary = models.CharField(max_length=200, blank=True, null=True)
    known_skills = models.ManyToManyField('skill.Skill', blank=True)

    def __str__(self):
        return self.username
