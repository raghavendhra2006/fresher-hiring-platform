from django.db import models
from accounts.models import CustomUser
from skill.models import Skill

class JobPost(models.Model):
    hr_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, default='Not Specified')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title

class ScreeningQuestion(models.Model):
    job = models.ForeignKey(JobPost, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    requires_yes = models.BooleanField()

    def __str__(self):
        return self.question_text

class JobApplication(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    match_rating = models.IntegerField()
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    hr_remark = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title} ({self.match_rating}%)"

    @property
    def match_category(self):
        if self.match_rating >= 80:
            return 'Strong Match'
        elif self.match_rating >= 50:
            return 'Skill Gap'
        else:
            return 'Not Recommended'
