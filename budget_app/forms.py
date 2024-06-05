from django import forms
from .models import Budget, CashEarned, Expense

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount']
        
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        
        model = Expense
        fields = ['description', 'amount', 'budget']
        
        
class CashEarnedForm(forms.ModelForm):
    class Meta:
        model = CashEarned
        fields = ['amount', 'description']