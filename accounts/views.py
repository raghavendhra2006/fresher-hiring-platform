from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from skill.models import Skill

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_fresher:
                return redirect('onboarding')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def onboarding_view(request):
    if not request.user.is_fresher:
        return redirect('home')
        
    if request.method == 'POST':
        experience = request.POST.get('experience_summary', '').strip()
        custom_skills_str = request.POST.get('custom_skills', '')
        
        request.user.experience_summary = experience
        request.user.save()
        
        if custom_skills_str:
            custom_list = [s.strip() for s in custom_skills_str.split(',') if s.strip()]
            for s_name in custom_list:
                normalized_name = s_name.title()
                skill_obj, created = Skill.objects.get_or_create(name__iexact=normalized_name, defaults={'name': normalized_name})
                request.user.known_skills.add(skill_obj)
                
        return redirect('home')
        
    return render(request, 'accounts/onboarding.html')
