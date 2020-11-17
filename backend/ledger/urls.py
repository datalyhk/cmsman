from django.urls import path
from . import views

app_name = 'ledger'
urlpatterns = [
    path('expense/category/<int:pk>/update/', views.ExpenseCategoryUpdate.as_view(), name='ExpenseCategoryUpdate'),
    path('expense/category/', views.ExpenseCategoryList.as_view(), name='ExpenseCategoryList'),
    path('expense/export/csv/', views.ExpenseExportCsv, name='ExpenseExportCsv'),
    path('expense/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='ExpenseUpdate'),
    path('expense/<int:pk>/update/modal/', views.ExpenseUpdateModal.as_view(), name='ExpenseUpdateModal'),
    path('expense/<int:pk>/delete/modal/', views.ExpenseDeleteModal.as_view(), name='ExpenseDeleteModal'),
    # path('expenses/vendor/<int:vendor_id>/new/', views.NewExpenseByVendorModal.as_view(), name='NewExpenseByVendorModal'),
    path('expense/new/modal/', views.NewExpenseModal.as_view(), name='NewExpenseModal'),
    path('expense/new/selectvendor/', views.NewExpenseSelectVendorView, name='NewExpenseSelectVendor'),
    path('expense/new/delivery/<int:delivery_id>/modal/', views.DeliveryPaymentModal.as_view(), name='DeliveryPaymentModal'),
    path('expense/<int:expense_id>/add/delivery/<int:delivery_id>/', views.ExpenseAddDeliveryOrder, name='ExpenseAddDeliveryOrder'),
    path('expense/<int:expense_id>/remove/delivery/<int:delivery_id>/', views.ExpenseRemoveDeliveryOrder, name='ExpenseRemoveDeliveryOrder'),
    path('expense/<int:pk>/', views.ExpenseDetail.as_view(), name='ExpenseDetail'),
    path('expense/new/', views.NewExpense.as_view(), name='NewExpense'),
    path('expense/', views.ExpenseList.as_view(), name='ExpenseList'),
    ]