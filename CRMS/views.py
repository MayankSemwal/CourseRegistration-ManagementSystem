from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Course, Student, Order
from django.shortcuts import render, redirect, reverse
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    if request.session.get('last_login'):
        message = "Your last login was at: " + str(request.session.get('last_login'))
    else:
        message = "Your las login was more than one hour ago"
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'CRMS/index.html', {'top_list': top_list, 'message': message})


# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     list_courses = Course.objects.all().order_by('title')[:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of topics: ' + '</p>'
#     response.write(heading1)
#     for topic in top_list:
#         para = '<p>' + str(topic.id) + ': ' + str(topic.name) + '</p>'
#         response.write(para)
#
#     heading2 = '<br> <p>' + 'List of Courses' + '</p>'
#     response.write(heading2)
#     for course in list_courses:
#         para = '<p> <b>Title: </b>' + str(course.title) + ' <b> Price: </b>' \
#                + str(course.price) + '</p>'
#         response.write(para)
#
#     return response


# def about(request):
#     headline = '<h2> This is an E-learning Website! Search our Topics to find all available Courses. </h2>'
#     response = HttpResponse()
#     response.write(headline)
#     return response
def about(request):
    headline = 'This is an E-learning Website! Search our Topics to find all available Courses.'
    about_visits = request.session.get('about_visits', 1)
    request.session['about_visits'] = about_visits + 1
    request.session.set_expiry(300)
    context = {'headline': headline, 'about_visits': about_visits}
    return render(request, 'CRMS/about.html', {'context': context})


# def detail(request, topic_id):
#     response = HttpResponse()
#     try:
#         topic = Topic.objects.get(id=topic_id)
#         name = '<h2>' + str(topic.name).upper() + '</h2>'
#         response.write(name)
#         len_topic = '<p><b>Length: </b>' + str(topic.length) + '</p>'
#         response.write(len_topic)
#         courses = Course.objects.filter(topic=topic_id)
#         para = '<p>' + '<b>Courses:</b>' + '</p>'
#         response.write(para)
#         for course in courses:
#             list_course = '<p> &emsp;&emsp;' + str(course.title) + '</p>'
#             response.write(list_course)
#     except Topic.DoesNotExist:
#         response = get_object_or_404(Topic, pk=topic_id)
#
#     return response

def detail(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    courses = Course.objects.filter(topic=topic_id)
    return render(request, 'CRMS/detail.html', {'topic': topic, 'courses': courses})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # print(name)
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']

            if length:
                topics = Topic.objects.filter(length=length)
            else:
                topics = Topic.objects.all()

            courselist = []
            for top in topics:
                courselist = courselist + list(top.courses.filter(price__lte=max_price))

            return render(request, 'CRMS/results.html', {'courselist': courselist, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'CRMS/findcourses.html', {'form': form})


@login_required(login_url='/user_login', redirect_field_name='next')
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.student
            email = student.email
            status = order.order_status
            temp_dic = {0: 'Cancelled', 1: 'Confirmed', 2: 'On Hold' }
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)

                msg_html = render_to_string('CRMS/order_conf_temp.html', {'student': student, 'courses': courses, 'status': temp_dic[status]})
                send_mail(
                    'Order status',
                    msg_html,
                    'admin@sender.com',
                    [email],
                    html_message=msg_html,
                )
            return render(request, 'CRMS/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'CRMS/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'CRMS/place_order.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if rating >= 1 and rating <= 5:
                reveiw = form.save(commit=True)
                course = form.cleaned_data['course']
                course.num_reviews += 1
                reveiw.save()
                course.save()
                return redirect('/')
            else:
                return render(request, 'CRMS/review.html',
                              {'form': form, 'message': "You must enter a rating between 1 and 5!"})
        else:
            return render(request, 'CRMS/review.html', {'form': form, 'message': "Form not valied!"})
    else:
        form = ReviewForm()
        return render(request, 'CRMS/review.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username + " "+ password)
        user = authenticate(username=username, password=password)
        # print(user)
        if user:
            if user.is_active:
                login(request, user)
                current_time = datetime.datetime.now()
                request.session['last_login'] = str(current_time)[:-7]
                request.session['username'] = username
                request.session['fullname'] = str(user.first_name + ' ' + user.last_name).title() # Project: 7
                request.session.set_expiry(3600)
                # project: 5
                if request.POST.get('next', ''):
                    return HttpResponseRedirect(request.POST.get('next', ''))
                else:
                    return HttpResponseRedirect(reverse('CRMS:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'CRMS/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('CRMS:index')))

# project: 5
@login_required(login_url='/user_login', redirect_field_name='next')
def myaccount(request):
    username = request.session.get('username')
    if len(Student.objects.filter(username=username)) > 0:
        student = Student.objects.get(username=username)
        firstname = student.first_name
        lastname = student.last_name
        topics = student.interested_in.all()
        courses = student.registered_courses.all()
        image = student.profile_image
        email = student.email
        address = student.address
        province = student.province
        print(image)
        return render(request, 'CRMS/myaccount.html', {'firstname': firstname, 'lastname': lastname,
                                                        'topics': topics, 'courses': courses, 'profile_image': image,
                                                        'address': address, 'province':province,'email':email})
    else:
        return render(request, 'CRMS/myaccount.html',
                      {'message': "You are not a registered student!"})


# Project :4
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = form.save()
            password = form.cleaned_data['password']
            student.set_password(password)
            student.save()
            return HttpResponseRedirect(reverse('myapp:user_login'))
    else:
        form = RegisterForm()
    return render(request, 'CRMS/register.html', {'form': form})
