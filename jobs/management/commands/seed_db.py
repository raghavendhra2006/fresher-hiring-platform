from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from skill.models import Skill
from jobs.models import JobPost, ScreeningQuestion, JobApplication
import random

class Command(BaseCommand):
    help = 'Seeds the database with synthetic data for presentation.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")
        CustomUser.objects.all().delete()
        Skill.objects.all().delete()
        JobPost.objects.all().delete()
        
        self.stdout.write("Creating Users...")
        hr_user = CustomUser.objects.create_superuser(
            username='hr_admin', email='hr@test.com', password='admin123', is_hr=True
        )
        fresher_user = CustomUser.objects.create_user(
            username='fresher_user', email='fresher@test.com', password='admin123', is_fresher=True
        )
        
        # Mock candidates
        mock_candidates = []
        for i in range(5):
            u = CustomUser.objects.create_user(
                username=f'mock_candidate_{i}', email=f'mock{i}@test.com', password='admin123', is_fresher=True
            )
            mock_candidates.append(u)
            
        self.stdout.write("Generating Skills...")
        skill_names = [
            'Python', 'Django', 'SQL', 'React', 'Git', 
            'TypeScript', 'AWS', 'Docker', 'Linux', 'HTML',
            'CSS', 'JavaScript', 'Node.js', 'PostgreSQL', 'Figma'
        ]
        
        skills = []
        for name in skill_names:
            skills.append(Skill.objects.create(name=name, demand_score=random.randint(10, 100)))

        self.stdout.write("Generating Job Posts & Questions...")
        job_data = [
            ("Frontend Developer", "Building dynamic web interfaces.", 4),
            ("Backend Engineer", "Designing fast APIs.", 4),
            ("Full Stack Dev", "End to end web development.", 5),
            ("Data Engineer", "Working with data pipelines.", 3),
            ("DevOps Specialist", "Optimizing our deployments.", 3),
        ]
        
        for title, desc, num_skills in job_data:
            job = JobPost.objects.create(
                hr_author=hr_user,
                title=title,
                description=desc,
                is_active=True
            )
            job.skills.set(random.sample(skills, num_skills))
            
            # Screening questions
            for _ in range(random.randint(3, 4)):
                ScreeningQuestion.objects.create(
                    job=job,
                    question_text=f"Do you have over 1 year of experience in {random.choice(skill_names)}?",
                    requires_yes=random.choice([True, True, False])
                )
                
            # Applications
            for c in random.sample(mock_candidates, random.randint(1, 3)):
                JobApplication.objects.create(
                    candidate=c,
                    job=job,
                    match_rating=random.randint(40, 100),
                    status=random.choice(['Pending', 'Accepted', 'Rejected'])
                )
                
        self.stdout.write(self.style.SUCCESS("Successfully seeded the database!"))
