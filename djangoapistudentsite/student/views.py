import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

def student_list(request):
    try:
        # সার্চ ফাংশনালিটি
        search_query = request.GET.get('search', '')
        if search_query:
            response = requests.get(f"{settings.API_BASE_URL}students/search/?search={search_query}")
        else:
            response = requests.get(f"{settings.API_BASE_URL}students/")
            
        students = response.json() if response.status_code == 200 else []
        return render(request, 'student/list.html', {
            'students': students,
            'search_query': search_query
        })
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API Connection Error: {str(e)}")
        return render(request, 'student/list.html', {'students': []})

def add_student(request):
    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'roll_number': request.POST.get('roll_number')
            }
            response = requests.post(f"{settings.API_BASE_URL}students/", data=data)
            
            if response.status_code == 201:
                messages.success(request, "Student added successfully!")
                return redirect('student_list')
            else:
                error_data = response.json()
                for field, errors in error_data.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API Connection Error: {str(e)}")
    
    return render(request, 'student/add.html')

def edit_student(request, student_id):
    # স্টুডেন্ট ডিটেইলস পেতে
    try:
        response = requests.get(f"{settings.API_BASE_URL}students/{student_id}/")
        if response.status_code != 200:
            messages.error(request, "Student not found")
            return redirect('student_list')
            
        student = response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API Connection Error: {str(e)}")
        return redirect('student_list')

    # আপডেট রিকোয়েস্ট হ্যান্ডলিং
    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'roll_number': request.POST.get('roll_number')
            }
            response = requests.put(f"{settings.API_BASE_URL}students/{student_id}/", data=data)
            
            if response.status_code == 200:
                messages.success(request, "Student updated successfully!")
                return redirect('student_list')
            else:
                error_data = response.json()
                for field, errors in error_data.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API Connection Error: {str(e)}")
    
    return render(request, 'student/edit.html', {'student': student})

def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            response = requests.delete(f"{settings.API_BASE_URL}students/{student_id}/")
            if response.status_code == 204:
                messages.success(request, "Student deleted successfully!")
            else:
                messages.error(request, "Failed to delete student")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API Connection Error: {str(e)}")
    
    return redirect('student_list')