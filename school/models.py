from django.db import models

from django.contrib.auth.models import User
import uuid


class Student(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    profile_image = models.ImageField(max_length=3000, upload_to='profiles/', null=True, blank=True)
    gender = models.CharField(max_length=7, choices=[('M', ('Male')), ('F', ('Female')), ('O', ('Others'))], default='Others')
    bio = models.TextField(max_length=200, null=True, blank=True)
    
    
    def display_profile_image(self):
        try:
            return self.profile_image.url
        except:
            return '/static/img/user-default.png'
    
    def __str__(self) -> str:
        return  '%s  %s' %(self.firstname,self.lastname)
    
class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    course = models.CharField(max_length=40)
    course_cover = models.ImageField(max_length=3000, upload_to='course_cover/')
    slug = models.SlugField()
    about = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def have_paid(self):
        return self.paidcourses_set.values_list('student_name__id', flat=True)
    
    def __str__(self):
        return self.course
    
    
class CourseSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.session_name


class CourseVideo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_sid = models.ForeignKey(CourseSession, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=400)
    video = models.FileField(max_length=60000, upload_to='courses/')
    duration = models.IntegerField()
    date =  models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title

class PaidCourses(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    date =  models.DateTimeField(auto_now_add=True)
    
    
    

    
    
class ContactForm(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=300)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=600)
    date =  models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student = models.ManyToManyField(Student)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    read = models.ManyToManyField(Student, related_name='is_read', null=True, blank=True)
    date =  models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering= ['-date']
        
class CertificationRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    date =  models.DateTimeField(auto_now_add=True)