from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    if request.user.is_fresher:
        return redirect('candidate_dashboard')
    elif request.user.is_hr:
        return redirect('hr_dashboard')
    # Default fallback, log them out if they have no role
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')
