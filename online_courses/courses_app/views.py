from django.shortcuts import render
from django.http import HttpResponse

dummy_users = [
    {
        'id': 0,
        'username': 'MokrykY',
        'firstname': 'Yaroslav',
        'lastname': 'Mokryk',
        'email': 'stornstornstorn@gmail.com',
        'password': 'mokrykpassword',
        'is_teacher': '0'
    },
    {
        'id': 1,
        'username': 'KhavalkoV',
        'firstname': 'Victor',
        'lastname': 'Khavalko',
        'email': 'khavalko@nulp.edu',
        'password': 'khavalkopassword',
        'is_teacher': '1'
    },
    {
        'id': 2,
        'username': 'BerdnykD',
        'firstname': 'Danylo',
        'lastname': 'Berdnyk',
        'email': 'berdnyk@nulp.edu',
        'password': 'berdnykpassword',
        'is_teacher': '0'
    },
    {
        'id': 3,
        'username': 'DavidM',
        'firstname': 'David',
        'lastname': 'Malan',
        'email': 'davidmalan@harvard.edu',
        'password': 'malanpassword',
        'is_teacher': '1'
    },
]

dummy_courses = [
    {
        'id': 0,
        'name': 'CS50',
        'teacher': 3,
        'students': [
            0,
        ]
    },
    {
        'id': 1,
        'name': 'Applied Programming',
        'teacher': 1,
        'students': [
            0,
            2,
        ]
    },
]

dummy_applications = [
    {
        'id': 0,
        'course': 0,
        'student': 2,
        'status': 'placed' # Placed/Approved/Rejected
    },
    {
        'id': 1,
        'course': 1,
        'student': 2,
        'status': 'approved' # Placed/Approved/Rejected
    },
]

def home(request):
    context = {'dummy_courses': dummy_courses, 'users': dummy_users}
    return render(request, 'courses_app/home.html', context)
def courseId(request, id):
    if request.method == 'POST' and request.POST.get('delete') == 'Delete':
        return HttpResponse('<h3>200 - Success! Course was deleted.</h3>', status=200)
    myCourse = {}
    for course in dummy_courses:
        if course['id'] == id:
            myCourse = course
            break
    context = {'course': myCourse, 'users': dummy_users}
    return render(request, 'courses_app/courseId.html', context)
def appId(request, id):
    if request.method == 'POST' and request.POST.get('approve') == 'Approve':
        return HttpResponse('<h3>200 - Success! Application was approved.</h3>', status=200)
    elif request.method == 'POST' and request.POST.get('reject') == 'Reject':
        return HttpResponse('<h3>200 - Success! Application was rejected.</h3>', status=200)
    myApp = {}
    for app in dummy_applications:
        if app['id'] == id:
            myApp = app
            break
    context = {'app': myApp, 'users': dummy_users}
    return render(request, 'courses_app/appId.html', context)
def courses(request):
    context = {'users': dummy_users}
    if request.method == 'POST':
        data = request.POST.copy()
        studs = data.get('students').split(',')
        if len(studs) > 5:
            return HttpResponse('<h3>400 - Too many students! Max 5 students per course.</h3>', status=400)
        return HttpResponse('<h3>201 - Success! Course created.</h3>', status=201)
    return render(request, 'courses_app/courses.html', context)
def createApp(request, id):
    curUser = {}
    for user in dummy_users:
        if user['id'] == id:
            curUser = user
            break
    context = {'user': curUser, 'courses': dummy_courses}
    if request.method == 'POST':
        data = request.POST.copy()
        return HttpResponse('<h3>201 - Success! Application created.</h3>', status=201)
    return render(request, 'courses_app/createApp.html', context)
def logout(request):
    context = {}
    if request.method == 'POST':
        return HttpResponse('<h3>200 - Success! Logged out.</h3>', status=200)
    return render(request, 'courses_app/logout.html', context)
def login(request):
    context = {'users': dummy_users}
    if request.method == 'POST':
        data = request.POST.copy()
        curUser = {}
        for user in dummy_users:
            if user['username'] == data.get('username'):
                curUser = user
                break
        if data.get('password') == curUser['password']:
            return HttpResponse('<h3>200 - Success! Logged in.</h3>', status=200)
        return HttpResponse('<h3>403 - Forbidden! Wrong password.</h3>', status=403)
    return render(request, 'courses_app/login.html', context)
def createUser(request):
    if request.method == 'POST':
        data = request.POST.copy()
        for user in dummy_users:
            if user['username'] == data.get('username'):
                return HttpResponse('<h3>403 - Forbidden! User already exists.', status = 403)
        return HttpResponse('<h3>201 - Success! Created user.</h3>', status=201)
    return render(request, 'courses_app/createUser.html')