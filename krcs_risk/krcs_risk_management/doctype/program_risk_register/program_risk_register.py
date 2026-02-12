# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, add_months, getdate, date_diff, nowdate


RISK_LEVEL_MATRIX = [
    (1,  4,  "Low"),
    (5,  9,  "Medium"),
    (10, 14, "High"),
    (15, 25, "Critical"),
]

# Days ahead to warn "Due Soon"
DUE_SOON_DAYS = 7

FREQUENCY_OFFSETS = {
    "Daily":       {"days": 1},
    "Weekly":      {"days": 7},
    "Fortnightly": {"days": 14},
    "Monthly":     {"months": 1},
    "Quarterly":   {"months": 3},
    "Semi-Annual": {"months": 6},
    "Annual":      {"months": 12},
}

# Statuses where the record is locked for editing by non-approvers
LOCKED_STATUSES = ("Pending Approval", "Pending Close Approval", "Closed")

# Roles that grant approval ability (mirrors api.py constants)
GLOBAL_APPROVER_ROLES = {"KRCS HOR", "KRCS DSG", "System Manager"}
DEPT_APPROVER_ROLES   = {"KRCS HOD"}
PROJECT_APPROVER_ROLES = {"KRCS Project Manager"}
ALL_APPROVER_ROLES = GLOBAL_APPROVER_ROLES | DEPT_APPROVER_ROLES | PROJECT_APPROVER_ROLES


def get_risk_level(rating):
    """Return risk level label based on overall rating (likelihood x impact, scale 1-25)."""
    for low, high, label in RISK_LEVEL_MATRIX:
        if low <= rating <= high:
            return label
    return ""


def calculate_next_review_due(last_review_date, frequency):
    """Calculate the next review due date from a given date and frequency."""
    if not last_review_date or not frequency:
        return None
    offset = FREQUENCY_OFFSETS.get(frequency)
    if not offset:
        return None
    if "days" in offset:
        return add_days(last_review_date, offset["days"])
    if "months" in offset:
        return add_months(last_review_date, offset["months"])
    return None


def compute_review_status(next_review_due):
    """Return On Track / Due Soon / Overdue based on next_review_due vs today."""
    if not next_review_due:
        return "Not Scheduled"
    diff = date_diff(next_review_due, today())
    if diff < 0:
        return "Overdue"
    if diff <= DUE_SOON_DAYS:
        return "Due Soon"
    return "On Track"


def _is_any_approver():
    """Return True if the current user has any approver role."""
    roles = set(frappe.get_roles(frappe.session.user))
    return bool(roles & ALL_APPROVER_ROLES)


class ProgramRiskRegister(Document):
    def validate(self):
        # --- Prevent editing locked records by non-approvers ---
        if self.get_doc_before_save():
            old_status = self.get_doc_before_save().status
            if old_status in LOCKED_STATUSES and not _is_any_approver():
                frappe.throw(
                    f"This risk is currently <b>{old_status}</b> and cannot be edited. "
                    "Only a Risk Approver can change it.",
                    frappe.PermissionError,
                )

        # --- Risk rating ---
        likelihood = self.likelihood or 0
        impact = self.impact or 0
        self.overall_rating = likelihood * impact
        if self.overall_rating:
            self.risk_level = get_risk_level(self.overall_rating)
        else:
            self.risk_level = ""

        # --- Review schedule ---
        self._update_review_schedule()

    def _update_review_schedule(self):
        """Auto-calculate next_review_due from the latest review and the frequency."""
        frequency = self.review_frequency

        # Find the most recent review date from child table
        latest_date = None
        if self.risk_reviews:
            dates = [
                getdate(r.review_date)
                for r in self.risk_reviews
                if r.review_date
            ]
            if dates:
                latest_date = max(dates)

        if frequency and latest_date:
            self.next_review_due = calculate_next_review_due(latest_date, frequency)
        elif frequency and not latest_date:
            # No reviews yet — next review due from today
            self.next_review_due = calculate_next_review_due(today(), frequency)
        else:
            self.next_review_due = None

        self.review_status = compute_review_status(self.next_review_due)
