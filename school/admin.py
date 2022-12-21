from django.contrib import admin
from .models import *

class studentAdmin(admin.ModelAdmin):
    exclude = ['']
    
    fieldsets = [
        ('Important Details', {'fields': ['firstname','lastname', 'user', 'email']}),
        ('Pherepheral', {'fields': ['profile_image','gender', 'bio'], 'classes': ['collapse']})
    ]
    
    list_display= ('user', 'firstname','lastname',  'email', 'gender')
    search_fields = ['firstname','lastname', 'email', 'gender']
admin.site.register(Student, studentAdmin)

@admin.register(Course)
class CourserAdmin(admin.ModelAdmin):
    list_display= ('course', 'date')
    prepopulated_fields = {'slug': ('course',), }

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'video')

@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'session_name', 'date')
    
@admin.register(ContactForm)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date')


@admin.register(PaidCourses)
class PaidCouresAdmin(admin.ModelAdmin):
    list_display=('course_id', 'student_name', 'date')

@admin.register(Notification)
class PaidCouresAdmin(admin.ModelAdmin):
    list_display=('subject', 'date')
    

@admin.register(CertificationRequest)
class PaidCouresAdmin(admin.ModelAdmin):
    list_display=('student_name', 'date')
    