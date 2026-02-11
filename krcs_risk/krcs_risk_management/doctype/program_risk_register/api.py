# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def add_risk_review(risk_name, review_date, reviewed_by, summary, actions, next_review_date=None):
    """
    Add a new review to a risk register
    """
    try:
        # Get the risk register document
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)

        # Add new review row
        risk_doc.append("risk_reviews", {
            "review_date": review_date,
            "reviewed_by": reviewed_by,
            "summary": summary,
            "actions": actions,
            "next_review_date": next_review_date
        })

        # Save the document
        risk_doc.save()

        return {
            "success": True,
            "message": "Review added successfully",
            "risk": risk_doc.as_dict()
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error adding risk review"))
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def update_risk_review(risk_name, review_idx, review_date, reviewed_by, summary, actions, next_review_date=None):
    """
    Update an existing review in a risk register
    """
    try:
        # Get the risk register document
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)

        # Find and update the review
        review_idx = int(review_idx)
        if review_idx < len(risk_doc.risk_reviews):
            risk_doc.risk_reviews[review_idx].review_date = review_date
            risk_doc.risk_reviews[review_idx].reviewed_by = reviewed_by
            risk_doc.risk_reviews[review_idx].summary = summary
            risk_doc.risk_reviews[review_idx].actions = actions
            risk_doc.risk_reviews[review_idx].next_review_date = next_review_date

            # Save the document
            risk_doc.save()

            return {
                "success": True,
                "message": "Review updated successfully",
                "risk": risk_doc.as_dict()
            }
        else:
            return {
                "success": False,
                "message": "Review not found"
            }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error updating risk review"))
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def delete_risk_review(risk_name, review_idx):
    """
    Delete a review from a risk register
    """
    try:
        # Get the risk register document
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)

        # Remove the review
        review_idx = int(review_idx)
        if review_idx < len(risk_doc.risk_reviews):
            risk_doc.risk_reviews.pop(review_idx)

            # Save the document
            risk_doc.save()

            return {
                "success": True,
                "message": "Review deleted successfully",
                "risk": risk_doc.as_dict()
            }
        else:
            return {
                "success": False,
                "message": "Review not found"
            }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error deleting risk review"))
        return {
            "success": False,
            "message": str(e)
        }
