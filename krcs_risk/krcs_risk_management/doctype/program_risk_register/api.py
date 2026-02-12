# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate

# ---------------------------------------------------------------------------
# Role constants
# ---------------------------------------------------------------------------

# Global approvers: can approve any risk regardless of department/project
GLOBAL_APPROVER_ROLES = {"KRCS HOR", "KRCS DSG", "System Manager"}

# Department-scoped approvers: can only approve risks in their own department
DEPT_APPROVER_ROLES = {"KRCS HOD"}

# Project-scoped approvers: can only approve risks on their own project(s)
PROJECT_APPROVER_ROLES = {"KRCS Project Manager"}

# All roles that grant any approval ability
ALL_APPROVER_ROLES = GLOBAL_APPROVER_ROLES | DEPT_APPROVER_ROLES | PROJECT_APPROVER_ROLES


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_user_roles():
    """Return the set of roles for the current session user."""
    return set(frappe.get_roles(frappe.session.user))


def _is_global_approver(roles=None):
    """Return True if the user has a global approver role."""
    if roles is None:
        roles = _get_user_roles()
    return bool(roles & GLOBAL_APPROVER_ROLES)


def _get_employee_department(user):
    """
    Return the Department linked to the given user's Employee record, or None.
    Looks up Employee where 'user_id' == user.
    """
    emp = frappe.db.get_value(
        "Employee", {"user_id": user, "status": "Active"}, "department"
    )
    return emp or None


def _get_employee_projects(user):
    """
    Return a set of Project names where the user is listed as Project Manager.
    Checks the Project DocType field 'project_manager' (Link to User).
    """
    projects = frappe.get_all(
        "Project",
        filters={"project_manager": user, "status": ["!=", "Cancelled"]},
        pluck="name",
    )
    return set(projects)


def _can_approve(risk_doc, roles=None):
    """
    Return True if the current user is eligible to approve/reject the given risk.

    Rules:
    - Global roles (KRCS HOR, KRCS DSG, System Manager): any risk
    - KRCS HOD: only risks whose department matches the user's Employee department
    - KRCS Project Manager: only risks whose project matches a project managed by the user
    """
    if roles is None:
        roles = _get_user_roles()

    # Global approvers always qualify
    if _is_global_approver(roles):
        return True

    user = frappe.session.user

    # Department-scoped: HOD
    if roles & DEPT_APPROVER_ROLES:
        user_dept = _get_employee_department(user)
        if user_dept and user_dept == risk_doc.department:
            return True

    # Project-scoped: Project Manager
    if roles & PROJECT_APPROVER_ROLES:
        user_projects = _get_employee_projects(user)
        if risk_doc.project and risk_doc.project in user_projects:
            return True

    return False


# ---------------------------------------------------------------------------
# Approval workflow endpoints
# ---------------------------------------------------------------------------

@frappe.whitelist()
def submit_for_approval(risk_name):
    """
    Move a risk from Draft/Rejected → Pending Approval.
    Any logged-in user who can read the doc may submit.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        if doc.status not in ("Draft", "Rejected"):
            return {"success": False, "message": f"Cannot submit a risk with status '{doc.status}'."}
        doc.db_set("status", "Pending Approval")
        doc.db_set("rejection_reason", "")
        frappe.db.commit()
        return {"success": True, "message": "Risk submitted for approval.", "status": "Pending Approval"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error submitting risk for approval"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def request_close(risk_name):
    """
    Move a risk from Open → Pending Close Approval.
    Any logged-in user who can read the doc may request closure.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        if doc.status != "Open":
            return {"success": False, "message": f"Cannot request closure for a risk with status '{doc.status}'."}
        doc.db_set("status", "Pending Close Approval")
        frappe.db.commit()
        return {"success": True, "message": "Closure requested.", "status": "Pending Close Approval"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error requesting risk closure"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def approve_risk(risk_name):
    """
    Approve a pending risk.
    Pending Approval → Open
    Pending Close Approval → Closed
    Requires an approver role scoped to this risk.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        if not _can_approve(doc):
            frappe.throw(_("You do not have permission to approve this risk."), frappe.PermissionError)
        if doc.status == "Pending Approval":
            new_status = "Open"
        elif doc.status == "Pending Close Approval":
            new_status = "Closed"
        else:
            return {"success": False, "message": f"Risk is not pending approval (status: '{doc.status}')."}
        doc.db_set("status", new_status)
        doc.db_set("approved_by", frappe.session.user)
        doc.db_set("approval_date", nowdate())
        doc.db_set("rejection_reason", "")
        frappe.db.commit()
        return {"success": True, "message": f"Risk approved and set to {new_status}.", "status": new_status}
    except frappe.PermissionError:
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error approving risk"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def reject_risk(risk_name, reason=""):
    """
    Reject a pending risk.
    Pending Approval → Rejected
    Pending Close Approval → Open
    Requires an approver role scoped to this risk.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        if not _can_approve(doc):
            frappe.throw(_("You do not have permission to reject this risk."), frappe.PermissionError)
        if doc.status == "Pending Approval":
            revert_status = "Rejected"
        elif doc.status == "Pending Close Approval":
            revert_status = "Open"
        else:
            return {"success": False, "message": f"Risk is not pending approval (status: '{doc.status}')."}
        doc.db_set("status", revert_status)
        doc.db_set("approved_by", frappe.session.user)
        doc.db_set("approval_date", nowdate())
        doc.db_set("rejection_reason", reason or "")
        frappe.db.commit()
        return {"success": True, "message": f"Risk rejected and set to {revert_status}.", "status": revert_status}
    except frappe.PermissionError:
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error rejecting risk"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_user_roles():
    """
    Return roles of the current user relevant to the approval workflow.
    Returns whether the user has ANY approver role (not scoped to a specific risk).
    Use can_approve_risk() to check per-risk eligibility.
    """
    roles = _get_user_roles()
    return {
        "is_any_approver": bool(roles & ALL_APPROVER_ROLES),
        "is_global_approver": _is_global_approver(roles),
        "roles": list(roles),
    }


@frappe.whitelist()
def can_approve_risk(risk_name):
    """
    Return whether the current user can approve/reject the specific risk.
    This is the per-risk scoped check used by the Vue dashboard and Frappe desk.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        eligible = _can_approve(doc)
        return {
            "can_approve": eligible,
            "status": doc.status,
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error checking approval eligibility"))
        return {"can_approve": False, "status": ""}


# ---------------------------------------------------------------------------
# Review endpoints
# ---------------------------------------------------------------------------

@frappe.whitelist()
def add_risk_review(risk_name, review_date, reviewed_by, summary, actions, next_review_date=None):
    """Add a new review to a risk register."""
    try:
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)
        risk_doc.append("risk_reviews", {
            "review_date": review_date,
            "reviewed_by": reviewed_by,
            "summary": summary,
            "actions": actions,
            "next_review_date": next_review_date
        })
        risk_doc.save()
        return {
            "success": True,
            "message": "Review added successfully",
            "risk": risk_doc.as_dict()
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error adding risk review"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_risk_review(risk_name, review_idx, review_date, reviewed_by, summary, actions, next_review_date=None):
    """Update an existing review in a risk register."""
    try:
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)
        review_idx = int(review_idx)
        if review_idx < len(risk_doc.risk_reviews):
            risk_doc.risk_reviews[review_idx].review_date = review_date
            risk_doc.risk_reviews[review_idx].reviewed_by = reviewed_by
            risk_doc.risk_reviews[review_idx].summary = summary
            risk_doc.risk_reviews[review_idx].actions = actions
            risk_doc.risk_reviews[review_idx].next_review_date = next_review_date
            risk_doc.save()
            return {
                "success": True,
                "message": "Review updated successfully",
                "risk": risk_doc.as_dict()
            }
        else:
            return {"success": False, "message": "Review not found"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error updating risk review"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def delete_risk_review(risk_name, review_idx):
    """Delete a review from a risk register."""
    try:
        risk_doc = frappe.get_doc("Program Risk Register", risk_name)
        review_idx = int(review_idx)
        if review_idx < len(risk_doc.risk_reviews):
            risk_doc.risk_reviews.pop(review_idx)
            risk_doc.save()
            return {
                "success": True,
                "message": "Review deleted successfully",
                "risk": risk_doc.as_dict()
            }
        else:
            return {"success": False, "message": "Review not found"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error deleting risk review"))
        return {"success": False, "message": str(e)}


# ---------------------------------------------------------------------------
# Admin helper
# ---------------------------------------------------------------------------

def _require_system_manager():
    """Raise PermissionError if the current user is not System Manager."""
    if "System Manager" not in _get_user_roles():
        frappe.throw(_("Only System Managers can perform this action."), frappe.PermissionError)


# ---------------------------------------------------------------------------
# Department & Unit management endpoints
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_departments():
    """
    Return all Departments with their Units.
    Available to all logged-in users (read-only lookup).
    """
    departments = frappe.get_all(
        "Department",
        fields=["name", "department_name"],
        order_by="department_name asc"
    )
    units = frappe.get_all(
        "Unit",
        fields=["name", "unit_name", "department"],
        order_by="unit_name asc"
    )
    # Attach units to departments
    unit_map = {}
    for u in units:
        unit_map.setdefault(u["department"], []).append(u)
    for dept in departments:
        dept["units"] = unit_map.get(dept["name"], [])
    return departments


@frappe.whitelist()
def create_department(department_name):
    """Create a new Department. System Manager only."""
    _require_system_manager()
    try:
        if frappe.db.exists("Department", {"department_name": department_name}):
            return {"success": False, "message": f"Department '{department_name}' already exists."}
        doc = frappe.get_doc({"doctype": "Department", "department_name": department_name})
        doc.insert()
        frappe.db.commit()
        return {"success": True, "message": "Department created.", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating department"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def delete_department(name):
    """Delete a Department (only if no linked risks). System Manager only."""
    _require_system_manager()
    try:
        if frappe.db.exists("Program Risk Register", {"department": name}):
            return {"success": False, "message": "Cannot delete: risks are linked to this department."}
        if frappe.db.exists("Unit", {"department": name}):
            return {"success": False, "message": "Cannot delete: units are linked to this department. Delete units first."}
        frappe.delete_doc("Department", name)
        frappe.db.commit()
        return {"success": True, "message": "Department deleted."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error deleting department"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def create_unit(unit_name, department):
    """Create a new Unit under a Department. System Manager only."""
    _require_system_manager()
    try:
        if frappe.db.exists("Unit", {"unit_name": unit_name}):
            return {"success": False, "message": f"Unit '{unit_name}' already exists."}
        doc = frappe.get_doc({"doctype": "Unit", "unit_name": unit_name, "department": department})
        doc.insert()
        frappe.db.commit()
        return {"success": True, "message": "Unit created.", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating unit"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def delete_unit(name):
    """Delete a Unit. System Manager only."""
    _require_system_manager()
    try:
        frappe.delete_doc("Unit", name)
        frappe.db.commit()
        return {"success": True, "message": "Unit deleted."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error deleting unit"))
        return {"success": False, "message": str(e)}


# ---------------------------------------------------------------------------
# User management endpoints
# ---------------------------------------------------------------------------

# KRCS roles that are managed via this admin panel
KRCS_ROLES = [
    "KRCS HOR",
    "KRCS DSG",
    "KRCS HOD",
    "KRCS Project Manager",
    "KRCS RPC",
    "KRCS Finance Officer",
    "KRCS Procurement Manager",
    "KRCS Logistics Manager",
    "KRCS HR Manager",
]


@frappe.whitelist()
def get_users():
    """
    Return all non-system users with their KRCS roles.
    System Manager only.
    """
    _require_system_manager()
    users = frappe.get_all(
        "User",
        filters={"name": ["not in", ["Guest", "Administrator"]], "user_type": "System User"},
        fields=["name", "full_name", "email", "enabled", "creation"],
        order_by="full_name asc"
    )
    # Attach roles to each user
    for u in users:
        roles = frappe.get_all(
            "Has Role",
            filters={"parent": u["name"], "role": ["in", KRCS_ROLES]},
            pluck="role"
        )
        u["krcs_roles"] = roles
    return users


@frappe.whitelist()
def create_user(email, first_name, last_name="", roles=None):
    """
    Create a new System User and assign KRCS roles.
    System Manager only.
    roles: JSON string of role names list.
    """
    _require_system_manager()
    import json
    try:
        if frappe.db.exists("User", email):
            return {"success": False, "message": f"User '{email}' already exists."}
        role_list = json.loads(roles) if isinstance(roles, str) else (roles or [])
        doc = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "user_type": "System User",
            "send_welcome_email": 0,
            "roles": [{"role": r} for r in role_list if r in KRCS_ROLES],
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "User created.", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating user"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_user_roles(user, roles=None):
    """
    Replace the KRCS roles for an existing user.
    roles: JSON string of role names list.
    System Manager only.
    """
    _require_system_manager()
    import json
    try:
        role_list = json.loads(roles) if isinstance(roles, str) else (roles or [])
        # Validate roles
        role_list = [r for r in role_list if r in KRCS_ROLES]

        user_doc = frappe.get_doc("User", user)
        # Remove existing KRCS roles
        user_doc.roles = [r for r in user_doc.roles if r.role not in KRCS_ROLES]
        # Add new KRCS roles
        for r in role_list:
            user_doc.append("roles", {"role": r})
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "Roles updated."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error updating user roles"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def toggle_user_enabled(user, enabled):
    """Enable or disable a user account. System Manager only."""
    _require_system_manager()
    try:
        enabled_val = int(enabled) if not isinstance(enabled, bool) else (1 if enabled else 0)
        frappe.db.set_value("User", user, "enabled", enabled_val)
        frappe.db.commit()
        state = "enabled" if enabled_val else "disabled"
        return {"success": True, "message": f"User {state}."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error toggling user"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_admin_meta():
    """
    Return metadata needed by the admin panel:
    - KRCS roles list
    - Whether current user is System Manager
    """
    roles = _get_user_roles()
    return {
        "is_system_manager": "System Manager" in roles,
        "krcs_roles": KRCS_ROLES,
    }
