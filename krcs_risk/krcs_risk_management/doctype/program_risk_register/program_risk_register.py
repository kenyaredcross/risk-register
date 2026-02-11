# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


RISK_LEVEL_MATRIX = [
    (1,  4,  "Low"),
    (5,  9,  "Medium"),
    (10, 14, "High"),
    (15, 25, "Critical"),
]


def get_risk_level(rating):
    """Return risk level label based on overall rating (likelihood x impact, scale 1-25)."""
    for low, high, label in RISK_LEVEL_MATRIX:
        if low <= rating <= high:
            return label
    return ""


class ProgramRiskRegister(Document):
    def validate(self):
        likelihood = self.likelihood or 0
        impact = self.impact or 0

        self.overall_rating = likelihood * impact

        if self.overall_rating:
            self.risk_level = get_risk_level(self.overall_rating)
        else:
            self.risk_level = ""
