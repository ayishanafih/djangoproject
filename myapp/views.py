from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User  # Import User model
from django.db.models import Q  # Import Q for query filtering
from .models import Course  # Assuming you have models for Course 
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Students
from .models import ExamSchedule
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods



def index(request):
    return render(request, 'index.html')

def adminclick_view(request):
    # Redirect authenticated users to the admin dashboard
    if request.user.is_authenticated:
        return redirect('admin-dashboard')
    return redirect('adminlogin')

def afterlogin_view(request):
    # Assuming this is for handling post-login redirects
    return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')

def custom_logout_view(request):
    logout(request)
    return redirect('adminlogin')

def admin_reset_password(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        new_password = request.POST['new_password']

        try:
            # Check if the username_or_email exists in the User model
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            # If the user is not found, show an error message
            messages.error(request, 'Admin not found with the provided username or email.')
            return redirect('admin_reset_password')

        # Update the user's password
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password reset successful.')
        return redirect('adminlogin')  # Redirect to login page or any other appropriate page

    return render(request, 'admin/reset_password.html')


@login_required(login_url='adminlogin')
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        # Save the course name to the database
        new_course = Course(course_name=course_name)
        new_course.save()

        # Add a success message
        messages.success(request, 'Course added successfully!')

        # Redirect to the same page or another page
        return redirect('add_course')  # Adjust this to your desired URL

    return render(request, 'admin/add_course.html')  # Renders the form template


# View Courses
@login_required(login_url='adminlogin')
def view_course(request):
    course = Course.objects.all()  # Fetch all course data
    return render(request, 'admin/view_course.html', {'course': course})  # Pass the data in context

@login_required(login_url='adminlogin')
@csrf_exempt  # For testing only. Remove in production.
def update_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course_name = request.POST.get('course_name')
        course.course_name = course_name
        course.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required(login_url='adminlogin')
@csrf_exempt  # For testing only. Remove in production.
def delete_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# Add Student View

@login_required(login_url='adminlogin')
def add_students(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        course_name = request.POST.get('course_name')

       
        # Save the form data to the Student model
        Students.objects.create(
            student_id=student_id,
            student_name=student_name,
            dob=dob,
            address=address,
            phone=phone,
            course_name=course_name
        )

        # Show success message
        messages.success(request, 'Student details successfully added!')

        # Redirect to the form page or another page after successful submission
        return redirect('add_students')

    return render(request, 'admin/add_students.html')

# View Students
@login_required(login_url='adminlogin')
def view_students(request):
    students = Students.objects.all()  # Retrieve all students
    return render(request, 'admin/view_students.html', {'students': students})


# Exam startdate
@login_required(login_url='adminlogin')
def exam_startdate(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        student_name = request.POST.get('student_name')
        start_date = request.POST.get('start_date')
        exam_date = request.POST.get('exam_date')
        
        # Save the data to the database
        exam_schedule = ExamSchedule(
            course_name=course_name,
            student_name=student_name,
            start_date=start_date,
            exam_date=exam_date
        )
        exam_schedule.save()
        
         # Show success message
        messages.success(request, 'Exam Scheduled successfully !')

        # Redirect to the form page or another page after successful submission
        return redirect('exam_startdate')
    
    return render(request, 'admin/exam_startdate.html')

@login_required(login_url='adminlogin')
def view_examdate(request):
    exam_data = ExamSchedule.objects.all()
    return render(request, 'admin/view_examdate.html', {'exam_data': exam_data})

@login_required(login_url='adminlogin')
def delete_exam(request, exam_id):
    if request.method == "POST":
        exam = get_object_or_404(ExamSchedule, id=exam_id)
        exam.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
@login_required(login_url='adminlogin')
@csrf_exempt
def edit_exam(request, exam_id):
    exam = get_object_or_404(ExamSchedule, id=exam_id)
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        student_name = request.POST.get('student_name')
        start_date = request.POST.get('start_date')
        exam_date = request.POST.get('exam_date')

        exam.course_name = course_name
        exam.student_name = student_name
        exam.start_date = start_date
        exam.exam_date = exam_date
        exam.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
def admin_404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

