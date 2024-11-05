"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from myapp import views
from django.contrib.auth.views import LogoutView,LoginView
from myapp.views import adminclick_view, admin_dashboard_view, admin_404,admin_reset_password,add_course,view_course,update_course,delete_course,add_students,view_students,exam_startdate,view_examdate,delete_exam,edit_exam

urlpatterns = [
   
    path('', views.index , name='index'),
     # add these lines
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='admin/login.html'),name='adminlogin'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin-dashboard', admin_dashboard_view, name='admin-dashboard'),
    path('admin_reset_password/', admin_reset_password, name='admin_reset_password'),
    path('admin/404', admin_404),
    path('add-course/', views.add_course, name='add_course'),
    path('view-course/', view_course, name='view_course'),
    path('update-course/<int:course_id>/', update_course, name='update_course'),
    path('delete-course/<int:course_id>/', delete_course, name='delete_course'),
    path('add-students/', views.add_students, name='add_students'),
    path('view-students/', views.view_students, name='view_students'),
    path('exam-startdate/', views.exam_startdate, name='exam_startdate'),
    path('view_examdate/', views.view_examdate, name='view_examdate'),
    path('delete-exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('edit-exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
   

]
    

