from rest_framework import serializers
from .models import Expense, Approval, ApprovalFlow, ApprovalStep, User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'company_id']

# Expense Serializer
class ExpenseSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = [
            'id', 'employee', 'company', 'amount', 'currency', 'converted_amount',
            'category', 'description', 'date_incurred', 'receipt', 'status',
            'chosen_flow', 'approvals', 'created_at', 'updated_at'
        ]
        read_only_fields = ['employee', 'status', 'approvals']

    def get_approvals(self, obj):
        approvals = obj.approvals.all().order_by('sequence_order')
        return [
            {
                "id": a.id,
                "approver": a.approver.username,
                "sequence_order": a.sequence_order,
                "status": a.status,
                "comments": a.comments,
                "approved_at": a.approved_at
            }
            for a in approvals
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['employee'] = user
        return super().create(validated_data)

# Approval Serializer
class ApprovalSerializer(serializers.ModelSerializer):
    expense = serializers.StringRelatedField()
    approver = serializers.StringRelatedField()

    class Meta:
        model = Approval
        fields = ['id', 'expense', 'approver', 'sequence_order', 'status', 'comments', 'approved_at']
        read_only_fields = ['expense', 'approver', 'sequence_order', 'approved_at']

# Approval Decision Serializer (for approve/reject)
class ApprovalDecisionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[Approval.STATUS_APPROVED, Approval.STATUS_REJECTED])
    comments = serializers.CharField(required=False, allow_blank=True)
