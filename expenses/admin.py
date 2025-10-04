from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Company, User, Expense, Approval, ApprovalFlow, ApprovalStep, ApprovalRule, OCRData, CurrencyRate

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "base_currency", "country", "created_at")

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("username", "email", "role", "company", "is_staff")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "company", "amount", "currency", "status", "date_incurred")
    list_filter = ("status", "company", "category")

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ("id", "expense", "approver", "sequence_order", "status", "approved_at")
    list_filter = ("status",)

admin.site.register(ApprovalFlow)
admin.site.register(ApprovalStep)
admin.site.register(ApprovalRule)
admin.site.register(OCRData)
admin.site.register(CurrencyRate)
