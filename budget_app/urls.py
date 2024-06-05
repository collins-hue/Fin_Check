from django.urls import path
from . import views

app_name = 'budget_app'
urlpatterns = [
    path('', views.set_budget, name='set_budget'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('budget-report/', views.budget_report, name='budget_report'),
    path('pdf-report/', views.generate_pdf_report, name='pdf_report'),
]
