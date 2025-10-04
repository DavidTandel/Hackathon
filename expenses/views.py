from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expense, Approval
from .serializer import ExpenseSerializer, ApprovalSerializer, ApprovalDecisionSerializer


from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Oddothon!")


# Permission: Only employee sees own expenses
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(employee=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

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
