from django.urls import path
from . import views

app_name = 'budget_app'
urlpatterns = [
    path('', views.budget_report, name='budget_report'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('add-expense/', views.add_expense, name='add_expense'),
        path('edit-cash-earned/<int:pk>/', views.edit_cash_earned, name='edit_cash_earned'),
    path('add-cash-earned/', views.add_cash_earned, name='add_cash_earned'),
    path('pdf-report/', views.generate_pdf_report, name='pdf_report'),
]
