from django.urls import path
from .views import home_view, hr_job_detail, job_apply, leaderboard_view, reapply_job, profile_view, hr_post_job, hr_add_questions

urlpatterns = [
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('hr/create-job/', hr_post_job, name='hr_post_job'),
    path('hr/job/<int:job_id>/questions/', hr_add_questions, name='hr_add_questions'),
    path('hr/job/<int:job_id>/', hr_job_detail, name='hr_job_detail'),
    path('apply/<int:job_id>/', job_apply, name='job_apply'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('reapply/<int:app_id>/', reapply_job, name='reapply_job'),
]
