# expenses/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# -- Company
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=128, blank=True, null=True)
    base_currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.base_currency})"


# -- User (custom, extends AbstractUser)
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_ADMIN = "Admin"
    ROLE_MANAGER = "Manager"
    ROLE_EMPLOYEE = "Employee"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_EMPLOYEE, "Employee"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'Company', null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="direct_reports",
    )
    is_manager_approver = models.BooleanField(default=False)

    # Add this to prevent reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='expenses_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='expenses_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

# -- Currency rate cache
class CurrencyRate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=20, decimal_places=8)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("base_currency", "target_currency")


# -- Approval flow template (admin config to define sequence)
class ApprovalFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="flows")
    name = models.CharField(max_length=255, default="Default Flow")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} / {self.name}"


class ApprovalStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(ApprovalFlow, on_delete=models.CASCADE, related_name="steps")
    sequence_order = models.PositiveIntegerField()
    # Either a specific approver or a role (Admin/Manager/Finance etc.)
    approver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    approver_role = models.CharField(max_length=32, null=True, blank=True,
                                     help_text="If set, resolves to users with this role")
    auto_escalate_after_hours = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("flow", "sequence_order")
        ordering = ["sequence_order"]


# -- Expense
class Expense(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_DRAFT = "Draft"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    date_incurred = models.DateField()
    receipt = models.FileField(upload_to="receipts/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    chosen_flow = models.ForeignKey(ApprovalFlow, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expense {self.id} - {self.employee} - {self.amount} {self.currency}"


# -- Approval instance (per expense)
class Approval(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"
    STATUS_SKIPPED = "Skipped"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_SKIPPED, "Skipped"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="approvals")
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="approvals_to_do")
    sequence_order = models.PositiveIntegerField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("expense", "approver")
        ordering = ["sequence_order"]


# -- Approval Rules (percentage, specific, hybrid)
class ApprovalRule(models.Model):
    RULE_PERCENTAGE = "Percentage"
    RULE_SPECIFIC = "Specific"
    RULE_HYBRID = "Hybrid"
    RULE_CHOICES = [
        (RULE_PERCENTAGE, "Percentage"),
        (RULE_SPECIFIC, "Specific"),
        (RULE_HYBRID, "Hybrid"),
    ]

    HYBRID_OR = "OR"
    HYBRID_AND = "AND"
    HYBRID_OPS = [(HYBRID_OR, "OR"), (HYBRID_AND, "AND")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="approval_rules")
    rule_type = models.CharField(max_length=20, choices=RULE_CHOICES)
    percentage_threshold = models.PositiveSmallIntegerField(null=True, blank=True,
                                                           help_text="0-100")
    specific_approver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                          on_delete=models.SET_NULL, related_name="specific_rules")
    hybrid_operator = models.CharField(max_length=3, choices=HYBRID_OPS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -- OCR extracted (optional)
class OCRData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="ocr_data")
    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    expense_date = models.DateField(null=True, blank=True)
    items_json = models.JSONField(null=True, blank=True)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    raw_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
