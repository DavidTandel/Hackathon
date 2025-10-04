# expenses/signals.py
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from .models import User, Company, Expense, Approval, ApprovalStep, ApprovalRule

# helper: get currency for country via restcountries API
def fetch_currency_for_country(country_name):
    try:
        r = requests.get(f"https://restcountries.com/v3.1/name/{country_name}?fields=name,currencies", timeout=5)
        r.raise_for_status()
        data = r.json()
        # first matching country's currencies
        if isinstance(data, list) and len(data) > 0:
            currencies = data[0].get("currencies", {})
            # currencies is dict of code -> {name, symbol}
            codes = list(currencies.keys())
            if codes:
                return codes[0]
    except Exception:
        pass
    return "USD"

# 1) Auto-create company when a user is created without company (first sign-up)
@receiver(post_save, sender=User)
def auto_create_company_for_user(sender, instance, created, **kwargs):
    if created and instance.company is None:
        # create a company automatically with username-based name (adjust as needed)
        currency = fetch_currency_for_country("United States")  # fallback; the signup flow should pass actual country
        company = Company.objects.create(name=f"{instance.username}'s Company", base_currency=currency)
        instance.company = company
        instance.role = User.ROLE_ADMIN
        instance.save(update_fields=["company", "role"])

# 2) When an expense is created and submitted (status Pending), create approval instances
@receiver(post_save, sender=Expense)
def generate_approvals_for_expense(sender, instance: Expense, created, **kwargs):
    if created and instance.status in (Expense.STATUS_PENDING,):
        # pick the chosen_flow if provided, else pick company's default flow
        flow = instance.chosen_flow or instance.company.flows.first()
        if flow:
            # create an Approval row for each step (resolve approver)
            for step in flow.steps.all():
                # If specific approver set in step -> use it; else resolve by role (first user with role)
                approver = None
                if step.approver_user:
                    approver = step.approver_user
                elif step.approver_role:
                    # pick first user in that role for now
                    approver = instance.company.users.filter(role=step.approver_role).first()
                if approver:
                    Approval.objects.create(expense=instance, approver=approver, sequence_order=step.sequence_order)

# 3) When an approval is saved/changed evaluate progression & conditional rules
@receiver(post_save, sender=Approval)
def on_approval_status_changed(sender, instance: Approval, **kwargs):
    expense = instance.expense

    # set approved_at timestamp for approved ones
    if instance.status == Approval.STATUS_APPROVED and instance.approved_at is None:
        instance.approved_at = timezone.now()
        instance.save(update_fields=["approved_at"])

    # Evaluate rules for expense
    evaluate_expense_rules(expense)


def evaluate_expense_rules(expense: Expense):
    """
    This function checks company's approval rules and marks expense Approved/Rejected
    when conditions are met. Implementation covers:
     - Specific approver rule (if the specific approver has approved)
     - Percentage rule (X% of approvers approved)
     - Hybrid (OR / AND) combination
    """
    rules = expense.company.approval_rules.all()
    approvals = list(expense.approvals.all())
    if not approvals:
        return

    total = len(approvals)
    approved_count = sum(1 for a in approvals if a.status == Approval.STATUS_APPROVED)
    # specific approvers approved?
    specific_ok = False
    for rule in rules:
        if rule.rule_type == ApprovalRule.RULE_SPECIFIC and rule.specific_approver:
            # check if that approver approved this expense
            for a in approvals:
                if a.approver_id == rule.specific_approver_id and a.status == Approval.STATUS_APPROVED:
                    specific_ok = True
                    break

    percentage_ok = False
    for rule in rules:
        if rule.rule_type == ApprovalRule.RULE_PERCENTAGE and rule.percentage_threshold:
            percentage_ok = (approved_count * 100 / total) >= rule.percentage_threshold

    # Hybrid handling: if a hybrid rule exists
    hybrid_ok = False
    for rule in rules:
        if rule.rule_type == ApprovalRule.RULE_HYBRID:
            p_ok = (approved_count * 100 / total) >= (rule.percentage_threshold or 100)
            s_ok = False
            if rule.specific_approver:
                for a in approvals:
                    if a.approver_id == rule.specific_approver_id and a.status == Approval.STATUS_APPROVED:
                        s_ok = True
                        break
            if rule.hybrid_operator == ApprovalRule.HYBRID_OR:
                hybrid_ok = p_ok or s_ok
            else:
                hybrid_ok = p_ok and s_ok

    # final decision precedence: Specific -> Hybrid -> Percentage -> sequential fallback
    if specific_ok or hybrid_ok or percentage_ok:
        # mark expense approved immediately
        expense.status = Expense.STATUS_APPROVED
        expense.save(update_fields=["status"])
        return

    # Sequential fallback: check if all approvals are approved (sequential end)
    if all(a.status == Approval.STATUS_APPROVED for a in approvals):
        expense.status = Expense.STATUS_APPROVED
        expense.save(update_fields=["status"])
        return

    # If any is rejected => mark expense rejected
    if any(a.status == Approval.STATUS_REJECTED for a in approvals):
        expense.status = Expense.STATUS_REJECTED
        expense.save(update_fields=["status"])
        return

    # Otherwise keep pending/in-progress
    # Optionally move to In Progress if first approver approved etc.
    # If first pending exists and some earlier are approved -> you might set In Progress
    if any(a.status == Approval.STATUS_APPROVED for a in approvals):
        expense.status = Expense.STATUS_IN_PROGRESS
        expense.save(update_fields=["status"])
