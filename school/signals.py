from django.contrib.auth.models import User
from .models import Student
from django.db.models.signals import post_save,post_delete
from django.core.mail import  send_mail
from django.conf import  settings

def created(sender,instance,created,**kwargs):
    if created:
        user = instance
        student = Student.objects.create(
            user=user,
            firstname=user.first_name,
            lastname=user.last_name,
            username=user.username,
            email=user.email
        )
        subject="Programic"
        body="WELCOME"

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [student.email],
            fail_silently=False
        )
def updateUser(sender, instance,created,**kwargs):
    student = instance
    user = student.user
    if created == False:
        user.first_name = student.firstname
        user.last_name = student.lastname
        user.username = student.username
        user.email = student.email
        user.save()

def deleted(sender,instance,**kwargs):
    user = instance.user
    user.delete()


post_save.connect(created,sender=User)
post_save.connect(updateUser,sender=Student)
post_delete.connect(deleted,sender=Student)