from django.urls import path
from .views import ExpenseListCreateView, PendingApprovalListView, ApprovalDecisionView

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expenses-list-create'),
    path('approvals/', PendingApprovalListView.as_view(), name='pending-approvals'),
    path('approvals/<uuid:pk>/decision/', ApprovalDecisionView.as_view(), name='approval-decision'),
]


