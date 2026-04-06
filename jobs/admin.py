from django.contrib import admin
from .models import JobPost, ScreeningQuestion, JobApplication

class ScreeningQuestionInline(admin.TabularInline):
    model = ScreeningQuestion
    extra = 1

class JobPostAdmin(admin.ModelAdmin):
    inlines = [ScreeningQuestionInline]
    filter_horizontal = ('skills',)

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(ScreeningQuestion)
admin.site.register(JobApplication)
