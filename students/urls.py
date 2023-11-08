from django.urls import path
from . import views

urlpatterns = [
  path('', views.user_login, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('students/', views.students, name='students'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]