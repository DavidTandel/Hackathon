# from django.urls import path
# from .views import ExpenseListCreateView, PendingApprovalListView, ApprovalDecisionView

# urlpatterns = [
#     path('expenses/', ExpenseListCreateView.as_view(), name='expenses-list-create'),
#     path('approvals/', PendingApprovalListView.as_view(), name='pending-approvals'),
#     path('approvals/<uuid:pk>/decision/', ApprovalDecisionView.as_view(), name='approval-decision'),
# ]


from django.urls import path
from .views import (
    ExpenseListCreateView,
    PendingApprovalListView,
    ApprovalDecisionView,
    AdminRegisterView,
    CustomLoginView,  # Import your login view
    DashboardSummaryView
)

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expenses-list-create'),
    path('approvals/', PendingApprovalListView.as_view(), name='pending-approvals'),
    path('approvals/<uuid:pk>/decision/', ApprovalDecisionView.as_view(), name='approval-decision'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),  # Add this line for login
    path("register/", AdminRegisterView.as_view(), name="admin-register"),
     path("dashboard-summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),

]
