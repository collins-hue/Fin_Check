import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget, Expense, CashEarned
from .forms import BudgetForm, ExpenseForm, CashEarnedForm
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

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_report')
    else:
        form = ExpenseForm()
    return render(request, 'budget_app/add_expense.html', {'form': form})

def edit_cash_earned(request, pk):
    cash_earned = get_object_or_404(CashEarned, pk=pk)
    if request.method == "POST":
        form = CashEarnedForm(request.POST, instance=cash_earned)
        if form.is_valid():
            form.save()
            return redirect('budget_app:budget_report')
    else:
        form = CashEarnedForm(instance=cash_earned)
    return render(request, 'budget_app/edit_cash_earned.html', {'form': form})


def add_cash_earned(request):
    if request.method == "POST":
        form = CashEarnedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_app:budget_report')
    else:
        form = CashEarnedForm()
    return render(request, 'budget_app/add_cash_earned.html', {'form': form})

def budget_report(request):
    budgets = Budget.objects.all()
    expenses = Expense.objects.all()
    cash_earned = CashEarned.objects.all()
    total_expenses = sum(expense.amount for expense in expenses)
    total_cash_earned = sum(cash.amount for cash in cash_earned)
    remaining_budget = sum(budget.amount for budget in budgets) + total_cash_earned - total_expenses
    last_budget = budgets.last()  # Get the last budget

    return render(request, 'budget_app/budget_report.html', {
        'budgets': budgets,
        'last_budget': last_budget,  # Pass the last budget to the template
        'expenses': expenses,
        'cash_earned': cash_earned,
        'total_expenses': total_expenses,
        'total_cash_earned': total_cash_earned,
        'remaining_budget': remaining_budget,
    })

def generate_pdf_report(request):
    # Get the current month
    now = datetime.datetime.now()
    current_month = now.strftime('%B')
    current_year = now.year

    # Filter data by the current month
    expenses = Expense.objects.filter(created_at__month=now.month, created_at__year=now.year)
    budgets = Budget.objects.filter(created_at__month=now.month, created_at__year=now.year)
    cash_earned = CashEarned.objects.filter(created_at__month=now.month, created_at__year=now.year)

    total_expenses = sum(expense.amount for expense in expenses)
    total_cash_earned = sum(cash.amount for cash in cash_earned)
    total_budget = sum(budget.amount for budget in budgets)
    remaining_budget = total_budget + total_cash_earned - total_expenses

    # Company details
    company_name = "Murgor Collins Kirwa"
    company_address = "P.O BOX 140, KABARNET, Baringo, 30400"

    # Create the PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=budget_report_{current_month}_{current_year}.pdf'

    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)

    # Title
    p.drawString(200, 780, "Monthly Budget Report")

    # Company details
    p.setFont("Helvetica", 12)
    p.drawString(30, 760, company_name)
    p.drawString(30, 745, company_address)

    # Date
    p.drawString(480, 780, f"{current_month} {current_year}")

    # Add a line separator
    p.line(30, 730, 580, 730)

    # Budget summary
    p.drawString(30, 710, f"Total Budget: ${total_budget:.2f}")
    p.drawString(30, 695, f"Total Cash Earned: ${total_cash_earned:.2f}")
    p.drawString(30, 680, f"Total Expenses: ${total_expenses:.2f}")
    p.drawString(30, 665, f"Remaining Budget: ${remaining_budget:.2f}")

    # Add a line separator
    p.line(30, 650, 580, 650)

    # Expenses section
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, 630, "Expenses:")
    p.setFont("Helvetica", 12)
    y = 610
    for expense in expenses:
        p.drawString(30, y, f"{expense.description}: ${expense.amount:.2f} on {expense.created_at.date()}")
        y -= 20
        if y < 50:  # Add a new page if necessary
            p.showPage()
            y = 750

    # Add a line separator
    p.line(30, y-10, 580, y-10)
    y -= 30

    # Cash Earned section
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, y, "Cash Earned:")
    p.setFont("Helvetica", 12)
    y -= 20
    for cash in cash_earned:
        p.drawString(30, y, f"{cash.description}: ${cash.amount:.2f} on {cash.created_at.date()}")
        y -= 20
        if y < 50:  # Add a new page if necessary
            p.showPage()
            y = 750

    # Finish the PDF
    p.showPage()
    p.save()
    return response