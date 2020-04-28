from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import (
    ExpenseCategory,
    Expense
)

from .forms import (
    NewExpenseCategoryForm, ExpenseCategoryUpdateForm,
    # NewExpenseForm, ExpenseEntryForm,
)

class ExpenseCategoryList(ListView, LoginRequiredMixin):
    model = ExpenseCategory
    template_name = "ledger/expense_category_list.html"
    context_object_name = 'expense_category_list_obj'
    paginate_by = 20
    last_query = ''
    last_query_count = 0

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            self.last_query = query
            object_list = ExpenseCategory.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            self.last_query_count = object_list.count
        else:
            self.last_query = ''
            object_list = ExpenseCategory.objects.all()
            self.last_query_count = object_list.count
        return object_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['last_query'] = self.last_query
        data['last_query_count'] = self.last_query_count
        return data

class ExpenseCategoryUpdate(UpdateView, LoginRequiredMixin):
    model = ExpenseCategory
    form_class = ExpenseCategoryUpdateForm
    template_name = "ledger/expense_category_update.html"
    success_url = reverse_lazy('ledger:ExpenseCategoryList')

class ExpenseCategoryDelete(DeleteView, LoginRequiredMixin):
    model = ExpenseCategory
    template_name = "ledger/expense_category_confirm_delete.html"
    success_url = reverse_lazy('ledger:ExpenseCategoryList')

class NewExpenseCategory(CreateView, LoginRequiredMixin):
    """Add new vendor"""
    model = ExpenseCategory
    template_name = 'ledger/new_expense_category.html'
    form_class = NewExpenseCategoryForm
    success_url = reverse_lazy('ledger:ExpenseCategoryList')
