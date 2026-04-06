from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import JobPost, ScreeningQuestion, JobApplication
from skill.models import Skill, UnmatchedSearch
import string

def home_view(request):
    bot_reply = None
    
    if not request.user.is_authenticated or not getattr(request.user, 'is_hr', False):
        jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
        
        if request.method == 'POST' and 'chatbot' in request.POST:
            query = request.POST.get('query', '').strip()
            clean_query = query.lower()
            
            match_found = False
            for skill in Skill.objects.all():
                if skill.name.lower() in clean_query:
                    skill.demand_score += 1
                    skill.save()
                    bot_reply = f"Yes! {skill.name} is trending!"
                    match_found = True
                    break
            
            if not match_found and clean_query:
                unmatched, created = UnmatchedSearch.objects.get_or_create(term=query.strip())
                if not created:
                    unmatched.query_count += 1
                    unmatched.save()
                bot_reply = "I'm not familiar with that skill, but I've noted it!"

        return render(request, 'jobs/fresher_home.html', {
            'jobs': jobs,
            'bot_reply': bot_reply,
        })
        
    else:
        total_jobs = JobPost.objects.filter(hr_author=request.user).count()
        total_apps = JobApplication.objects.filter(job__hr_author=request.user).count()
        return render(request, 'jobs/hr_home.html', {
            'total_jobs': total_jobs,
            'total_apps': total_apps
        })

@login_required
def profile_view(request):
    error = None
    if getattr(request.user, 'is_hr', False):
        if request.method == 'POST':
            action = request.POST.get('action')
            app_id = request.POST.get('app_id')
            hr_remark = request.POST.get('hr_remark', '').strip()
            
            target_app = get_object_or_404(JobApplication, id=app_id, job__hr_author=request.user)
            
            if action == 'Reject' and not hr_remark:
                error = f"Error processing {target_app.candidate.username}: You must provide a remark when rejecting a candidate."
            else:
                if action == 'Accept':
                    target_app.status = 'Accepted'
                elif action == 'Reject':
                    target_app.status = 'Rejected'
                
                target_app.hr_remark = hr_remark
                target_app.save()
            return redirect('profile')

        jobs = JobPost.objects.filter(hr_author=request.user).order_by('-created_at')
        return render(request, 'jobs/hr_profile.html', {
            'jobs': jobs,
            'error': error
        })
    else:
        my_applications = JobApplication.objects.filter(candidate=request.user).order_by('-created_at')
        
        rejected_apps = my_applications.filter(status='Rejected')
        missing_skills = {}
        for app in rejected_apps:
            for skill in app.job.skills.all():
                missing_skills[skill.name] = missing_skills.get(skill.name, 0) + 1
        top_missing = sorted(missing_skills.items(), key=lambda x: x[1], reverse=True)[:3]
        top_missing_skills = [k for k, v in top_missing]
        
        return render(request, 'jobs/fresher_profile.html', {
            'my_applications': my_applications,
            'top_missing_skills': top_missing_skills
        })

@login_required
def hr_post_job(request):
    if not getattr(request.user, 'is_hr', False):
        return redirect('home')
        
    skills = Skill.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        selected_skills = request.POST.getlist('skills')
        
        job = JobPost.objects.create(
            hr_author=request.user,
            title=title,
            description=description,
            is_active=True
        )
        if selected_skills:
            job.skills.set(selected_skills)
            
        return redirect('hr_add_questions', job_id=job.id)
        
    return render(request, 'jobs/post_job.html', {'skills': skills})

@login_required
def hr_add_questions(request, job_id):
    if not getattr(request.user, 'is_hr', False):
        return redirect('home')
        
    job = get_object_or_404(JobPost, id=job_id, hr_author=request.user)
    
    if request.method == 'POST':
        for i in range(1, 4):
            q_text = request.POST.get(f'q{i}_text', '').strip()
            if q_text:
                q_req = request.POST.get(f'q{i}_yesno') == 'yes'
                ScreeningQuestion.objects.create(job=job, text=q_text, requires_yes=q_req)
        return redirect('profile')
        
    return render(request, 'jobs/post_job_questions.html', {'job': job})

@login_required
def hr_job_detail(request, job_id):
    if not getattr(request.user, 'is_hr', False):
        return redirect('home')
        
    job = get_object_or_404(JobPost, id=job_id, hr_author=request.user)
    error = None
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_question':
            q_text = request.POST.get('question_text', '').strip()
            req_yes = request.POST.get('requires_yes') == 'yes'
            if q_text:
                ScreeningQuestion.objects.create(
                    job=job,
                    text=q_text,
                    requires_yes=req_yes
                )
            return redirect('hr_job_detail', job_id=job.id)
            
        app_id = request.POST.get('app_id')
        hr_remark = request.POST.get('hr_remark', '').strip()
        
        target_app = get_object_or_404(JobApplication, id=app_id, job=job)
        
        if action == 'Reject' and not hr_remark:
            error = f"Error processing {target_app.candidate.username}: You must provide a remark when rejecting a candidate."
        else:
            if action == 'Accept':
                target_app.status = 'Accepted'
            elif action == 'Reject':
                target_app.status = 'Rejected'
            
            target_app.hr_remark = hr_remark
            target_app.save()
            return redirect('hr_job_detail', job_id=job.id)

    pending_apps = job.jobapplication_set.filter(status='Pending').order_by('-match_rating')
    processed_apps = job.jobapplication_set.exclude(status='Pending').order_by('-match_rating')
    questions = job.questions.all()

    return render(request, 'jobs/hr_job_detail.html', {
        'job': job,
        'questions': questions,
        'pending_apps': pending_apps,
        'processed_apps': processed_apps,
        'error': error
    })

def leaderboard_view(request):
    top_skills = Skill.objects.order_by('-demand_score')[:10]
    agg = Skill.objects.aggregate(Max('demand_score'))
    max_score = agg['demand_score__max'] or 1
    
    leaderboard = []
    for rank, skill in enumerate(top_skills, 1):
        percent = int((skill.demand_score / max_score) * 100)
        leaderboard.append({
            'rank': rank,
            'name': skill.name,
            'demand_score': skill.demand_score,
            'percent': percent,
        })
    return render(request, 'jobs/leaderboard.html', {'leaderboard': leaderboard})

@login_required
def job_apply(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    questions = job.questions.all()
    
    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()
        
        if total_questions > 0:
            for q in questions:
                answer = request.POST.get(f'question_{q.id}')
                if answer == 'yes' and q.requires_yes:
                    correct_answers += 1
                elif answer == 'no' and not q.requires_yes:
                    correct_answers += 1
            
            match_rating = int((correct_answers / total_questions) * 100)
        else:
            match_rating = 100
        
        resume_file = request.FILES.get('resume')
        
        JobApplication.objects.create(
            candidate=request.user,
            job=job,
            match_rating=match_rating,
            resume=resume_file
        )
        return redirect('profile')

    return render(request, 'jobs/job_apply.html', {
        'job': job,
        'questions': questions
    })

@login_required
def reapply_job(request, app_id):
    if request.method == 'POST':
        app = get_object_or_404(JobApplication, id=app_id, candidate=request.user)
        app.status = 'Pending'
        app.hr_remark = ''
        app.save()
    return redirect('profile')
