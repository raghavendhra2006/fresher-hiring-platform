from django.urls import path
from .views import signup_view, onboarding_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('onboarding/', onboarding_view, name='onboarding'),
]
