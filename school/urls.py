from django.urls import path,include
from . import views
from .utils import fourRandomDigits,alphaNumericLock



frd = fourRandomDigits()
anl = alphaNumericLock()


app_name = 'school'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
   
    path('about/', views.aboutPage.as_view(), name='about'),
    path('contact/', views.contactPage.as_view(), name='contact'),
    path(f'payment-complete/{frd}/{anl}/<slug:course>/', views.PaymentComplate, name='payment-complete'), 

    
    path('courses/', include([
        path('',views.Courses.as_view(), name='courses'),
        path('<slug:slug>/', views.singleCourse, name='single-course'),
        path('video/<slug:course>/', views.CourseSession, name='cvp'),
    ])),
    
    path('account/', include([
        path('create-account/', views.signUpPage, name='signup'),
        path('login/', views.loginPage.as_view(), name='login'),
        path('', views.profilePage.as_view(), name='profile'),
        path('edit-account/',views.editProfilePage, name='edit-account'),
        path('notification/',views.notificationPage.as_view(), name='notification'),
        path('notification/<str:pk>/',views.viewNotificationMessage.as_view(), name='single-notification'),
        path('certificate/<slug:course>/',views.CertificateForm, name='certificate-request'),
        path('logout/', views.logOutPage, name='logout'),
    ]))
]
