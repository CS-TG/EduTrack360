from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('students')
        else:
            # Return an error message or handle invalid login
            error_message = "Invalid username or password. Please try again."
            return render(request, 'students/login.html', {'error_message': error_message})

    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def students(request):
  return render(request, 'students/students.html', {
    'students': Student.objects.all()
  })

@login_required
def view_student(request, id):
  return redirect('login')

@login_required
def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_first_name = form.cleaned_data['first_name']
      new_last_name = form.cleaned_data['last_name']
      new_email = form.cleaned_data['email']
      new_field_of_study = form.cleaned_data['field_of_study']
      new_average = form.cleaned_data['average']

      new_student = Student(
        student_number=new_student_number,
        first_name=new_first_name,
        last_name=new_last_name,
        email=new_email,
        field_of_study=new_field_of_study,
        average = new_average
      )
      new_student.save()
      return render(request, 'students/add.html', {
        'form': StudentForm(),
        'success': True
      })
  else:
    form = StudentForm()
  return render(request, 'students/add.html', {
    'form': StudentForm()
  })

@login_required
def edit(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return render(request, 'students/edit.html', {
        'form': form,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = StudentForm(instance=student)
  return render(request, 'students/edit.html', {
    'form': form
  })

@login_required
def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student.delete()
  return redirect('login')

@login_required
def generate_pdf(request):
    # Create a BytesIO buffer to write PDF content
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer and define the page size
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Generate PDF content here
    students_data = []
    # Get the list of students from your database
    students = Student.objects.all()
    for student in students:
        student_info = [
            str(student.student_number),
            student.first_name,
            student.last_name,
            student.email,
            student.field_of_study,
            str(student.average),
        ]
        students_data.append(student_info)

    # Define the table data and style
    table_data = [
        ['Student Number', 'First Name', 'Last Name', 'Email', 'Field of Study', 'Average'],
        *students_data
    ]

    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#337ab7'),
                              ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), '#f5f5f5'),
                              ('GRID', (0, 0), (-1, -1), 1, '#000000')]))

    # Build the PDF document and return the response
    pdf.build([table])
    buffer.seek(0)

    # File response with appropriate content type and headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    # Write the PDF content to the response
    response.write(buffer.read())
    buffer.close()

    return response