import datetime
from django.shortcuts import render, redirect
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def set_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_app:budget_report')
    else:
        form = BudgetForm()
    return render(request, 'budget_app/set_budget.html', {'form': form})
     

def budget_report(request):
    budgets = Budget.objects.all()
    expenses = Expense.objects.all()
    total_expenses = sum(expense.amount for expense in expenses)
    remaining_budget = sum(budget.amount for budget in budgets) - total_expenses
    last_budget = budgets.last()  # Get the last budget

    return render(request, 'budget_app/budget_report.html', {
        'budgets': budgets,
        'last_budget': last_budget,  # Pass the last budget to the template
        'expenses': expenses,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
    })


        
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_app:budget_report')
    else:
        form = ExpenseForm()
    return render(request, 'budget_app/add_expense.html', {'form': form})


def generate_pdf_report(request):
    # Get the current month
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    # Filter expenses by the current month
    expenses = Expense.objects.filter(created_at__month=current_month, created_at__year=current_year)
    budgets = Budget.objects.filter(created_at__month=current_month, created_at__year=current_year)

    total_expenses = sum(expense.amount for expense in expenses)
    total_budget = sum(budget.amount for budget in budgets)
    remaining_budget = total_budget - total_expenses

    # Create the PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=budget_report_{current_month}_{current_year}.pdf'

    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, f"Monthly Budget Report: {now.strftime('%B')} {current_year}")
    p.drawString(100, 730, f"Total Expenses: ${total_expenses}")
    p.drawString(100, 710, f"Remaining Budget: ${remaining_budget}")

    p.drawString(100, 690, "Expenses:")
    y = 670
    for expense in expenses:
        p.drawString(100, y, f"{expense.description}: ${expense.amount} on {expense.created_at.date()}")
        y -= 20

    # Finish the PDF
    p.showPage()
    p.save()
    return response

