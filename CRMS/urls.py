from django.urls import path
from CRMS import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'CRMS'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:topic_id>', views.detail, name='detail'),
    path(r'findcourses', views.findcourses, name='findcourses'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'review', views.review, name='review'),
    path(r'user_login', views.user_login, name='user_login'),
    path(r'register', views.register, name='register'),
    path(r'user_logout', views.user_logout, name='user_logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
]

urlpatterns += staticfiles_urlpatterns()
