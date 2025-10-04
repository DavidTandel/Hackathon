from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expense, Approval
from .serializer import ExpenseSerializer, ApprovalSerializer, ApprovalDecisionSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, Company
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

def home(request):
    return HttpResponse("Welcome to Oddothon!")

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(employee=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)
        
# views.py
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        requested_role = request.data.get("role")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role != requested_role:
            return Response({"error": "Role mismatch."}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Create Django session
        login(request, user)
        
        return Response({
            "id": str(user.id),
            "username": user.username,
            "role": user.role,
            "company": user.company.name if user.company else "",
        }, status=status.HTTP_200_OK)

class AdminRegisterView(APIView):
    permission_classes = [permissions.AllowAny] 
    def post(self, request):
        company_name = request.data.get("companyName")
        admin_name = request.data.get("adminName")
        admin_email = request.data.get("adminEmail")
        country = request.data.get("country")
        currency = request.data.get("currency")
        password = request.data.get("password")
        if not all([company_name, admin_name, admin_email, password, country, currency]):
            return Response({"error": "All fields are required"}, status=400)
        if User.objects.filter(email=admin_email).exists():
            return Response({"error": "Email already exists"}, status=400)
        
        company = Company.objects.create(
            name=company_name, country=country, base_currency=currency
        )
        admin = User.objects.create_user(
            username=admin_email,  # or make a username logic
            email=admin_email,
            first_name=admin_name,
            role=User.ROLE_ADMIN,
            company=company,
            password=password
        )
        return Response({"success": True, "role": admin.role})
    
class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        user = request.user
        if not user.is_authenticated:
            print("bhia nahi he authenticated!!!")
            return Response({"detail": "Authentication credentials were not provided."}, status=401)

        role = getattr(user, "role", "Employee")
        print("he authenticated!!")

        if role == "Admin":
            submitted = Expense.objects.count()
            approved = Expense.objects.filter(status=Expense.STATUS_APPROVED).count()
            rejected = Expense.objects.filter(status=Expense.STATUS_REJECTED).count()
        elif role == "Manager":
            # Example: manager can see team, you may need manager logic
            team_ids = user.direct_reports.values_list("id", flat=True)
            submitted = Expense.objects.filter(employee__in=team_ids).count()
            approved = Expense.objects.filter(employee__in=team_ids, status=Expense.STATUS_APPROVED).count()
            rejected = Expense.objects.filter(employee__in=team_ids, status=Expense.STATUS_REJECTED).count()
        else:  # Employee
            submitted = Expense.objects.filter(employee=user).count()
            approved = Expense.objects.filter(employee=user, status=Expense.STATUS_APPROVED).count()
            rejected = Expense.objects.filter(employee=user, status=Expense.STATUS_REJECTED).count()

        return Response({
            "submitted": submitted,
            "approved": approved,
            "rejected": rejected,
        })



# Get pending approvals for current user
class PendingApprovalListView(generics.ListAPIView):
    serializer_class = ApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Approval.objects.filter(approver=user, status=Approval.STATUS_PENDING).order_by('sequence_order')


# Approve or Reject
class ApprovalDecisionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            approval = Approval.objects.get(pk=pk, approver=request.user)
        except Approval.DoesNotExist:
            return Response({"detail": "Approval not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ApprovalDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        approval.status = serializer.validated_data['status']
        approval.comments = serializer.validated_data.get('comments', '')
        approval.save()  # triggers signal to evaluate expense rules
        return Response({"detail": f"Approval {approval.status}"}, status=status.HTTP_200_OK)
