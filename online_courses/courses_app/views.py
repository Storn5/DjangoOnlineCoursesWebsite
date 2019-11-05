from django.shortcuts import render
from django.http import HttpResponse
from .models import Course, App
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

dummy_applications = {}
dummy_users, dummy_courses = {}, {}

def home(request):
    context = {'courses': Course.objects.all(), 'users': User.objects.all() }
    return render(request, 'courses_app/home.html', context)
def courseId(request, Cid):
    if Course.objects.filter(id=Cid).count() == 0:
        return HttpResponse('<h3>400 - Wrong ID! Check if the course ID is correct.</h3>', status=400)
    if not request.user.is_authenticated:
        return HttpResponse('<h3>403 - Forbidden! You need to log in to view courses.</h3>', status=403)
    myCourse = Course.objects.filter(id=Cid).first()
    if request.method == 'POST' and request.POST.get('delete') == 'Delete':
        if not request.user.groups.filter(name = 'Teachers').exists():
            return HttpResponse('<h3>403 - Forbidden! Only teachers can delete courses.</h3>', status=403)
        myCourse.delete()
        return HttpResponse('<h3>200 - Success! Course was deleted.</h3>', status=200)
    context = {'course': myCourse, 'users': User.objects.all(), 'current_user': request.user}
    return render(request, 'courses_app/courseId.html', context)
def appId(request, Aid):
    if App.objects.filter(id=Aid).count() == 0:
        return HttpResponse('<h3>400 - Wrong ID! Check if the application ID is correct.</h3>', status=400)
    if not request.user.is_authenticated:
        return HttpResponse('<h3>403 - Forbidden! You need to log in to approve/reject applications.</h3>', status=403)
    if request.method == 'POST' and not request.user.groups.filter(name = 'Teachers').exists():
        return HttpResponse('<h3>403 - Forbidden! Only teachers can approve/reject applications.</h3>', status=403)
    if request.method == 'POST' and request.POST.get('approve') == 'Approve':
        App.objects.filter(id=Aid).update(status='approved')
        send_mail(
            'Application approved!',
            'Your application for the ' + str(App.objects.filter(id=Aid).first()) + ' has been approved.',
            'stornstornstorn@gmail.com',
            [App.objects.filter(id=Aid).first().student.email],
            fail_silently=True,
        )
        return HttpResponse('<h3>200 - Success! Application was approved.</h3>', status=200)
    elif request.method == 'POST' and request.POST.get('reject') == 'Reject':
        App.objects.filter(id=Aid).update(status='rejected')
        send_mail(
            'Application rejected!',
            'Your application for the ' + str(App.objects.filter(id=Aid).first()) + ' has been rejected.',
            'stornstornstorn@gmail.com',
            [App.objects.filter(id=Aid).first().student.email],
            fail_silently=True,
        )
        return HttpResponse('<h3>200 - Success! Application was rejected.</h3>', status=200)
    myApp = App.objects.filter(id=Aid).first()
    context = {'app': myApp, 'users': User.objects.all(), 'current_user': request.user}
    return render(request, 'courses_app/appId.html', context)
def courses(request):
    if not request.user.is_authenticated:
        return HttpResponse('<h3>403 - Forbidden! You need to log in to create courses.</h3>', status=403)
    context = {'users': Course.objects.all(), 'current_user': request.user}
    if request.method == 'POST':
        data = request.POST.copy()
        studs = data.get('students').split(',')
        if not request.user.groups.filter(name = 'Teachers').exists():
            return HttpResponse('<h3>403 - Forbidden! Only teachers can create courses.</h3>', status=403)
        if len(studs) > 5:
            return HttpResponse('<h3>400 - Too many students! Max 5 students per course.</h3>', status=400)
        new_course = Course(name=data.get('name'), teacher=User.objects.filter(username=data.get('teacher')).first())
        new_course.save()
        for stud in studs:
            new_course.students.add(User.objects.filter(username=stud).first())
        return HttpResponse('<h3>201 - Success! Course created.</h3>', status=201)
    return render(request, 'courses_app/courses.html', context)
def createApp(request):
    if not request.user.is_authenticated:
        return HttpResponse('<h3>403 - Forbidden! You need to log in to apply for courses.</h3>', status=403)
    context = {'courses': Course.objects.all(), 'current_user': request.user}
    if request.method == 'POST':
        if not request.user.groups.filter(name = 'Students').exists():
            return HttpResponse('<h3>403 - Forbidden! Only students can apply for courses.</h3>', status=403)
        data = request.POST.copy()
        new_app = App(course=Course.objects.filter(id=data.get('course')).first(), student=request.user, status='placed')
        new_app.save()
        return HttpResponse('<h3>201 - Success! Application created.</h3>', status=201)
    return render(request, 'courses_app/createApp.html', context)
def my_logout(request):
    context = {'current_user': request.user}
    if request.method == 'POST':
        logout(request)
        return HttpResponse('<h3>200 - Success! Logged out.</h3>', status=200)
    return render(request, 'courses_app/logout.html', context)
def my_login(request):
    if request.method == 'POST':
        data = request.POST.copy()
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponse('<h3>200 - Success! Logged in.</h3>', status=200)
        return HttpResponse('<h3>403 - Forbidden! Wrong username or password.</h3>', status=403)
    return render(request, 'courses_app/login.html')
def createUser(request):
    if request.method == 'POST':
        data = request.POST.copy()
        for user in User.objects.all():
            if user.username == data.get('username'):
                return HttpResponse('<h3>403 - Forbidden! User already exists.', status = 403)
        new_user = User(username=data.get('username'), password=data.get('password'), email=data.get('email'), first_name=data.get('firstname'), last_name=data.get('lastname'))
        new_user.save()
        group = Group.objects.get(name='Students')
        if data.get('isTeacher') == '1':
            group = Group.objects.get(name='Teachers')
        new_user.groups.add(group)
        return HttpResponse('<h3>201 - Success! Created user.</h3>', status=201)
    return render(request, 'courses_app/createUser.html')