import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import JobPost, ScreeningQuestion, JobApplication
from skill.models import Skill

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with a robust dataset for the HireAssist presentation.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Clearing existing core data (JobPosts, Skills, JobApplications)..."))
        
        # 1. Clear Old Data
        JobApplication.objects.all().delete()
        ScreeningQuestion.objects.all().delete()
        JobPost.objects.all().delete()
        Skill.objects.all().delete()
        
        # 2. Generate 20+ Skills
        self.stdout.write(self.style.SUCCESS("Generating Skills..."))
        skill_names = [
            "Python", "Django", "JavaScript", "React", "PostgreSQL", 
            "Docker", "AWS", "Data Analysis", "Machine Learning", "Git", 
            "Agile", "REST APIs", "FastAPI", "HTML/CSS", "Tailwind", 
            "TypeScript", "Node.js", "SQL", "MongoDB", "Kubernetes"
        ]
        
        created_skills = []
        for name in skill_names:
            skill = Skill.objects.create(name=name, demand_score=random.randint(5, 100))
            created_skills.append(skill)
            
        # 3. Create Users (HR & Candidates)
        self.stdout.write(self.style.SUCCESS("Generating Users..."))
        
        # HR Users
        hr1, _ = User.objects.get_or_create(username='hr_technova', defaults={'email': 'hr@technova.com'})
        hr1.set_password('hireassist2026')
        hr1.is_hr = True
        hr1.save()
        
        hr2, _ = User.objects.get_or_create(username='hr_datasphere', defaults={'email': 'hr@datasphere.com'})
        hr2.set_password('hireassist2026')
        hr2.is_hr = True
        hr2.save()
        
        hr_users = [hr1, hr2]
        
        # Candidates
        candidates_data = [
            {'username': 'c_alex', 'summary': 'Recent CS Graduate looking for full-stack opportunities.'},
            {'username': 'c_sophia', 'summary': 'Junior Frontend Dev with 1 yr experience in React ecosystem.'},
            {'username': 'c_liam', 'summary': 'Data enthusiast seeking entry-level analysis or backend positions.'},
            {'username': 'c_emma', 'summary': 'Cloud computing trainee with AWS and Docker certifications.'}
        ]
        
        created_candidates = []
        for data in candidates_data:
            cand, _ = User.objects.get_or_create(username=data['username'], defaults={'email': f"{data['username']}@mail.com"})
            cand.set_password('hireassist2026')
            cand.is_hr = False
            cand.experience_summary = data['summary']
            cand.save()
            
            # Assign random skills
            c_skills = random.sample(created_skills, random.randint(3, 5))
            cand.known_skills.set(c_skills)
            created_candidates.append(cand)
            
        # 4. Generate 10+ Realistic Job Posts
        self.stdout.write(self.style.SUCCESS("Generating Job Posts..."))
        companies = ['TechNova', 'DataSphere Systems', 'CloudScale Inc', 'Apex Innovations']
        jobs_data = [
            ('Junior Python Backend Developer', 'Looking for a motivated fresher to architect APIs using Django and Postgres.', 1),
            ('React Frontend Intern', 'Build high-performance UIs spanning our digital products utilizing React and Tailwind.', 0),
            ('Data Analyst (Entry Level)', 'Execute raw SQL queries mapping massive datasets efficiently utilizing basic ML frameworks.', 1),
            ('DevOps Trainee', 'Deploy platforms rapidly securely using Docker and Kubernetes structures.', 1),
            ('Full-Stack Engineer (0-1 Yrs)', 'Manage completely isolated infrastructures using Node.js backend pipelines and React frontends.', 0),
            ('Database Administrator Intern', 'Optimizing unstructured databases utilizing MongoDB and robust caching tools.', 1),
            ('Junior Agile Project Manager', 'Run sprints efficiently integrating Agile tracking natively utilizing standard lifecycle frameworks.', 0),
            ('Cloud Architect Assistant', 'Map scalable nodes actively provisioning AWS core services directly via configurations.', 1),
            ('Machine Learning Engineer (Fresher)', 'Scale intelligent models securely spanning complex structural constraints natively.', 1),
            ('FastAPI Backend Intern', 'Draft minimal structural endpoints reliably executing modern pipeline architectures independently.', 0)
        ]
        
        created_jobs = []
        for title, desc, hr_index in jobs_data:
            job = JobPost.objects.create(
                hr_author=hr_users[hr_index],
                company_name=random.choice(companies),
                title=title,
                description=desc,
                is_active=True
            )
            # Assign skills
            j_skills = random.sample(created_skills, random.randint(3, 4))
            job.skills.set(j_skills)
            
            # 5. Add Screening Questions
            ScreeningQuestion.objects.create(job=job, question_text="Do you possess a basic understanding of the core requirements?", requires_yes=True)
            ScreeningQuestion.objects.create(job=job, question_text="Are you actively legally authorized to work locally?", requires_yes=True)
            
            created_jobs.append(job)
            
        # 6. Generate Mock Applications
        self.stdout.write(self.style.SUCCESS("Generating Application Pipelines..."))
        status_choices = ['Pending', 'Accepted', 'Rejected']
        remarks = [
            "Candidate displays outstanding technical aptitude.",
            "Lacking sufficient experience aligned locally with our stack.",
            "Great communication skills, strongly aligned technically.",
            "We are pursuing candidates matching different algorithmic requirements natively."
        ]
        
        for cand in created_candidates:
            # Apply to 2-3 random jobs
            applied_jobs = random.sample(created_jobs, random.randint(2, 3))
            for job in applied_jobs:
                stat = random.choice(status_choices)
                remark = random.choice(remarks) if stat != 'Pending' else ''
                
                # Mock a theoretical skill match manually
                match_val = random.randint(40, 100)
                
                JobApplication.objects.create(
                    candidate=cand,
                    job=job,
                    match_rating=match_val,
                    status=stat,
                    hr_remark=remark
                )

        self.stdout.write(self.style.SUCCESS("Database officially seeded perfectly! Ready for massive presentation."))
