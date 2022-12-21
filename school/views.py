from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from .forms import createAccountForm,EditAccountForm,StudentContactForm
from django.views.generic import View,ListView,TemplateView,DetailView,RedirectView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .models import Course,CourseVideo,Student,PaidCourses,CourseVideo,Notification,CertificationRequest
from django.db.models import Count,Sum,FloatField,DecimalField,IntegerField
import random
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .utils import unread_messages
from programic.settings import PAYSTACK_PUBLIC_KEY

site_logo = '/static/images/logo.png'


def signUpPage(request):
    form = createAccountForm()
    
    if request.method == 'POST':
        form = createAccountForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.username = student.username.lower()
            
            try:
                Student.objects.get(email=student.email)
                messages.info(request, 'a user is already using the email change it')
            except:
                student.save()
                login(request,student)
                messages.success(request, 'Account Created Successfully... Edit your Profile')
                return HttpResponseRedirect(reverse('school:edit-account'))
    context = {'form':form, 'logo':site_logo}
    return render(request, 'school/signup.html',context)

class loginPage(View):
    template_name = 'school/login.html'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('school:home')
        return render(request, self.template_name, {'logo':site_logo})
    
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(request, 'Welcome back %s' %username)
            return redirect(request.GET['next'] if 'next' in request.GET else '/account/')
        
        else:
            messages.error(request, 'username or password not correct')
            
        return render(request, self.template_name, {'logo':site_logo})
            

class Home(ListView):
    model  = Course
    template_name = 'school/index.html'
    context_object_name = 'courses'
    
    queryset = Course.objects.order_by('date')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = site_logo
        context['courses'] = Course.objects.all()
        return context


class Courses(ListView):
    model = Course
    template_name = 'school/course.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = site_logo
        context['courses'] = Course.objects.all()
        return context
    
    
def singleCourse(request, slug):
    try:
        student = request.user.student
    except:
        student = None
    course = Course.objects.get(slug=slug)
    related_courses = Course.objects.exclude(slug=slug)
    lectures = CourseVideo.objects.filter(course_id__slug=slug).aggregate(total=Count('video'))
    duration = CourseVideo.objects.filter(course_id__slug=slug).aggregate(mins=Sum('duration'))
    certificaterequests = CertificationRequest.objects.filter(course_id=course).values_list('student_name__id', flat=True)
    if request.method == 'POST':
        student = request.user.student
        payment = int(float(request.POST.get('course-price')))
        course = request.POST.get('course-name')
        course_info = Course.objects.get(course=course)
        ps_pk = PAYSTACK_PUBLIC_KEY
        
        context = { 'logo':site_logo,'student':student,'payment':payment, 'course':course, 'course_info':course_info, 'ps_pk':ps_pk}
        return render(request, 'school/confirm-payment.html',context)
        
    return render(request, 'school/detail.html', {
        'logo':site_logo,
        'course': course,
        'related_courses':related_courses,
        'lectures': lectures,
        'duration':duration ,
        'courses':Course.objects.all(),
        'student':student,
        'certificaterequests':certificaterequests
        }        
                    )
        
    
class aboutPage(TemplateView):
    template_name = 'school/about.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = site_logo
        context['courses'] = Course.objects.all()
        return context

@method_decorator(login_required(login_url='/account/login/') ,name='dispatch')
class profilePage(TemplateView):
    template_name = 'school/account.html'
    
    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = site_logo
        context['student'] = self.request.user.student
        context['paid_courses'] = self.request.user.student.paidcourses_set.all()
        context['recommended_courses'] = random.choices(k=3, population=Course.objects.order_by('-date'))
        context['is_notification'] = unread_messages(self,self.request)
        return context
    
    
@login_required(login_url='/account/login/')
def editProfilePage(request):
    student = request.user.student
    
    if request.method == 'POST':
        form = EditAccountForm(request.POST,request.FILES, instance=student)
        student = form.save(commit=False)
        if student.profile_image and student.profile_image.name.endswith(('.jpg', '.png', '.jpg')) or student.profile_image == '':
            student.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('school:profile')
        else:
            messages.error(request, 'Something went wrong. Try again later')
    else:
        form = EditAccountForm(instance=student)
    
    
    return render(request, 'school/edit-account.html',{'form':form, 'logo':site_logo})
 

@login_required(login_url='/account/login/')
def PaymentComplate(request, course):
        student_recipe = PaidCourses.objects.create(
            course_id = Course.objects.get(slug=course),
            student_name = request.user.student
        )
        student_recipe.save()
        purchase_notification = Notification.objects.create(
            subject="Course Purchase",
            message="you just purchase %s course start learning.. Thank you " %course
        )
        purchase_notification.student.add(request.user.student)
        purchase_notification.save()
        messages.success(request, '%s purchased successfully' %course)
        return redirect('/account/')
 
@login_required(login_url='/account/login/')
def CourseSession(request, course):
    student = request.user.student
    course = Course.objects.get(slug=course)
    if student.id not in course.have_paid():
        return HttpResponseRedirect(reverse('school:single-course', args=(course.slug,)))
    duration = course.coursevideo_set.aggregate(hrs=Sum('duration', output_field=IntegerField()) / 60, mins=Sum('duration') % 60, )
    lesson = course.coursevideo_set.count()
    context = {'course': course, 'duration':duration, 'lessons':lesson}
    return render(request, 'school/course-vlist.html', context)


class notificationPage(View):
    template_name = 'school/notification.html'
    
    
    def get(self, request, *args, **kwargs):
        student = self.request.user.student
        notification = student.notification_set.all()
        unread = unread_messages(self,request)
        context = {'notification':notification, 'total_unread':unread, 'logo':site_logo}
        return render(request, self.template_name, context)


class viewNotificationMessage(DetailView):
    model = Notification
    template_name = 'school/message.html'
    context_object_name = 'message'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_reading_notificaton = Notification.objects.get(id=self.kwargs.get('pk'))
        student_reading_notificaton.read.add(self.request.user.student)
        student_reading_notificaton.save()
        context['logo'] = site_logo
        return context

def CertificateForm(request, course):
    student = request.user.student
    course = Course.objects.get(slug=course)
    if student.id not in course.have_paid():
        messages.error(request, 'Something when wrong')
        return HttpResponseRedirect(reverse('school:single-course', args=(course.slug,)))
    else:
        certificaterequest = CertificationRequest.objects.create(
            student_name = student,
            course_id=course
        )
        certificaterequest.save()
        
        
        notification = Notification.objects.create(
            subject = 'Certificate Request',
            message = 'Response will be sent to your mail on your certificate'
        )
        notification.student.add(student)
        notification.save()
        messages.success(request, 'Certificate request have been submitted..check your notification page')
        return HttpResponseRedirect(reverse('school:single-course', args=(course.slug,)))
    
class contactPage(CreateView):
    form_class = StudentContactForm
    template_name = 'school/contact.html'
    success_url = '/contact/'
    
    def get_success_url(self) -> str:
        messages.success(self.request, 'message submitted successfully and would be respond to quickly')
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = site_logo
        context['form'] = self.form_class
        context['courses'] = Course.objects.all()
    
        return context
    
def logOutPage(request):
    logout(request)
    return redirect('/account/login/')