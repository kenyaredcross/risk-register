# Copyright (c) 2026, KRCS and contributors
# Scheduled tasks for KRCS Risk Management

import frappe
from frappe.utils import today, getdate, nowdate
from krcs_risk.krcs_risk_management.doctype.program_risk_register.program_risk_register import (
    compute_review_status,
    calculate_next_review_due,
)


def daily():
    """
    Daily scheduled task:
    1. Recompute review_status for all active risks.
    2. Send email notifications for Overdue and Due Soon risks.
    """
    _update_all_review_statuses()
    _send_review_notifications()


def _update_all_review_statuses():
    """Recalculate review_status on every active risk register."""
    risks = frappe.get_all(
        "Program Risk Register",
        filters={"status": "Active"},
        fields=["name", "next_review_due", "review_status"],
    )
    for risk in risks:
        new_status = compute_review_status(risk.next_review_due)
        if new_status != risk.review_status:
            frappe.db.set_value(
                "Program Risk Register",
                risk.name,
                "review_status",
                new_status,
                update_modified=False,
            )
    frappe.db.commit()


def _send_review_notifications():
    """
    Send email to Risk Owner (and their email) for risks that are Overdue or Due Soon.
    Only notifies once per day by checking if a notification was already sent today.
    """
    risks = frappe.get_all(
        "Program Risk Register",
        filters={
            "status": "Active",
            "review_status": ["in", ["Overdue", "Due Soon"]],
            "review_frequency": ["!=", ""],
        },
        fields=[
            "name", "project", "risk_description", "risk_level",
            "review_frequency", "next_review_due", "review_status",
            "risk_owner", "department",
        ],
    )

    if not risks:
        return

    # Group risks by owner so we send one email per owner
    owner_risks = {}
    for risk in risks:
        owner = risk.risk_owner
        if not owner:
            continue
        owner_risks.setdefault(owner, []).append(risk)

    for owner_name, owner_risks_list in owner_risks.items():
        # Get owner email
        owner_doc = frappe.db.get_value(
            "Risk Owner", owner_name, ["owner_name", "email"], as_dict=True
        )
        if not owner_doc or not owner_doc.get("email"):
            continue

        _send_owner_notification(owner_doc, owner_risks_list)


def _send_owner_notification(owner_doc, risks):
    """Compose and send a single email to an owner listing their due/overdue risks."""
    overdue = [r for r in risks if r.review_status == "Overdue"]
    due_soon = [r for r in risks if r.review_status == "Due Soon"]

    subject = f"[KRCS Risk Management] Review Alert — {len(overdue)} Overdue, {len(due_soon)} Due Soon"

    rows = ""
    for r in overdue + due_soon:
        status_label = (
            '<span style="color:#DC2626;font-weight:bold;">OVERDUE</span>'
            if r.review_status == "Overdue"
            else '<span style="color:#F59E0B;font-weight:bold;">DUE SOON</span>'
        )
        rows += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #eee;">{r.name}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{r.project or ''}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{r.risk_level or ''}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{r.review_frequency or ''}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{r.next_review_due or 'N/A'}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{status_label}</td>
        </tr>"""

    message = f"""
    <div style="font-family:Arial,sans-serif;max-width:700px;">
        <div style="background:#DC2626;padding:16px 24px;border-radius:8px 8px 0 0;">
            <h2 style="color:#fff;margin:0;">KRCS Risk Management — Review Alert</h2>
        </div>
        <div style="background:#fff;padding:24px;border:1px solid #e5e7eb;border-radius:0 0 8px 8px;">
            <p>Dear <strong>{owner_doc.owner_name}</strong>,</p>
            <p>The following risks assigned to you require your attention today ({today()}):</p>
            <table style="width:100%;border-collapse:collapse;margin-top:16px;">
                <thead>
                    <tr style="background:#f9fafb;">
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Risk ID</th>
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Project</th>
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Risk Level</th>
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Frequency</th>
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Next Review Due</th>
                        <th style="padding:8px;text-align:left;border-bottom:2px solid #e5e7eb;">Status</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
            <p style="margin-top:24px;">Please log in to the Risk Management Dashboard to conduct the review.</p>
            <p style="color:#6b7280;font-size:12px;margin-top:32px;">
                This is an automated notification from KRCS Risk Management System.
            </p>
        </div>
    </div>
    """

    try:
        frappe.sendmail(
            recipients=[owner_doc.email],
            subject=subject,
            message=message,
            now=True,
        )
    except Exception as e:
        frappe.log_error(
            f"Failed to send review notification to {owner_doc.email}: {e}",
            "Risk Review Notification"
        )
