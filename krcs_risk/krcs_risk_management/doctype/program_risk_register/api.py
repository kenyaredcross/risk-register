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

# Project-scoped approvers: can only approve risks on their managed project(s)
PROJECT_APPROVER_ROLES = {"KRCS Project Manager"}

# All roles that grant any approval ability
ALL_APPROVER_ROLES = GLOBAL_APPROVER_ROLES | DEPT_APPROVER_ROLES | PROJECT_APPROVER_ROLES

# Approval routing: who should approve based on who created the risk
# RPC creates → PM must approve
# PM creates  → HOD must approve
# All others  → HOD must approve (fallback)
CREATOR_TO_APPROVER = {
    "KRCS RPC": "KRCS Project Manager",
    "KRCS Project Manager": "KRCS HOD",
}
FALLBACK_APPROVER_ROLE = "KRCS HOD"


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


def _get_creator_primary_krcs_role(creator_user):
    """
    Return the most relevant KRCS role of the user who created the risk.
    Priority order matches CREATOR_TO_APPROVER keys.
    """
    roles = set(frappe.get_roles(creator_user))
    # Check in priority order
    for role in ("KRCS RPC", "KRCS Project Manager", "KRCS HOD", "KRCS HOR", "KRCS DSG"):
        if role in roles:
            return role
    return None


def _required_approver_role(risk_doc):
    """
    Return the role that is required to approve this specific risk, based on
    who created it:
      - Created by KRCS RPC       → KRCS Project Manager must approve
      - Created by KRCS Project Manager → KRCS HOD must approve
      - All other creators        → KRCS HOD must approve (fallback)

    Global approvers (KRCS HOR, KRCS DSG, System Manager) can always approve
    regardless of routing.
    """
    creator = risk_doc.owner  # Frappe always stores creator in 'owner'
    creator_role = _get_creator_primary_krcs_role(creator)
    return CREATOR_TO_APPROVER.get(creator_role, FALLBACK_APPROVER_ROLE)


def _can_approve(risk_doc, roles=None):
    """
    Return True if the current user is eligible to approve/reject the given risk.

    Routing rules (based on creator's role):
    - Risk created by KRCS RPC       → KRCS Project Manager who manages the
                                        risk's project (or any PM if no project)
    - Risk created by KRCS PM        → KRCS HOD of the risk's department
    - All other creators             → KRCS HOD of the risk's department (fallback)

    Global roles (KRCS HOR, KRCS DSG, System Manager) can always approve any risk.
    A user can never approve their own risk (self-approval is always denied).
    """
    if roles is None:
        roles = _get_user_roles()

    user = frappe.session.user

    # Self-approval is never allowed — the creator cannot approve their own risk
    if user == risk_doc.owner:
        return False

    # Global approvers qualify for any risk they didn't create
    if _is_global_approver(roles):
        return True

    required_role = _required_approver_role(risk_doc)

    if required_role == "KRCS Project Manager":
        # Must be a PM and manage this risk's project
        if "KRCS Project Manager" in roles:
            user_projects = _get_employee_projects(user)
            # If the risk has a project, PM must manage it; if no project, any PM qualifies
            if not risk_doc.project or risk_doc.project in user_projects:
                return True

    elif required_role == "KRCS HOD":
        # Must be an HOD in the same department as the risk
        if "KRCS HOD" in roles:
            user_dept = _get_employee_department(user)
            if user_dept and user_dept == risk_doc.department:
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
    Also returns the required approver role and self-approval flag for UI display.
    This is the per-risk scoped check used by the Vue dashboard and Frappe desk.
    """
    try:
        doc = frappe.get_doc("Program Risk Register", risk_name)
        is_own_risk = frappe.session.user == doc.owner
        eligible = _can_approve(doc)
        required_role = _required_approver_role(doc)
        return {
            "can_approve": eligible,
            "is_own_risk": is_own_risk,
            "status": doc.status,
            "awaiting_approver_role": required_role,
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error checking approval eligibility"))
        return {"can_approve": False, "is_own_risk": False, "status": "", "awaiting_approver_role": ""}


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
# Admin helpers
# ---------------------------------------------------------------------------

def _require_system_manager():
    """Raise PermissionError if the current user is not System Manager."""
    if "System Manager" not in _get_user_roles():
        frappe.throw(_("Only System Managers can perform this action."), frappe.PermissionError)


def _is_system_manager():
    """Return True if the current user is System Manager."""
    return "System Manager" in _get_user_roles()


def _get_current_user_department():
    """
    Return the krcs_department of the current session user's User record, or None.
    This is the department field set on the User doctype (not the Employee record).
    """
    return frappe.db.get_value("User", frappe.session.user, "krcs_department")


def _require_user_manager():
    """
    Raise PermissionError unless the current user is System Manager, KRCS HOD, or KRCS Project Manager.
    These roles are allowed to add/edit users within their own department.
    """
    roles = _get_user_roles()
    allowed = {"System Manager", "KRCS HOD", "KRCS Project Manager"}
    if not (roles & allowed):
        frappe.throw(_("You do not have permission to manage users."), frappe.PermissionError)


# Roles that HOD is allowed to assign when creating/editing users
_HOD_ASSIGNABLE_ROLES = {
    "KRCS HOD", "KRCS Project Manager", "KRCS RPC",
    "KRCS Finance Officer", "KRCS Procurement Manager",
    "KRCS Logistics Manager", "KRCS HR Manager",
}

# Roles that PM is allowed to assign when creating/editing users
_PM_ASSIGNABLE_ROLES = {
    "KRCS RPC",
    "KRCS Finance Officer", "KRCS Procurement Manager",
    "KRCS Logistics Manager", "KRCS HR Manager",
}


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
    """
    Create a new Unit under a Department.
    System Manager: any department.
    KRCS HOD: only their own department.
    """
    roles = _get_user_roles()
    is_sm = "System Manager" in roles
    is_hod = "KRCS HOD" in roles
    if not is_sm and not is_hod:
        frappe.throw(_("Only System Managers or HODs can create units."), frappe.PermissionError)
    if not is_sm and is_hod:
        own_dept = _get_current_user_department()
        if not own_dept or department != own_dept:
            return {"success": False, "message": "You can only add units to your own department."}
    try:
        if frappe.db.exists("Unit", {"unit_name": unit_name}):
            return {"success": False, "message": f"Unit '{unit_name}' already exists."}
        doc = frappe.get_doc({"doctype": "Unit", "unit_name": unit_name, "department": department})
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "Unit created.", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating unit"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def delete_unit(name):
    """
    Delete a Unit.
    System Manager: any unit.
    KRCS HOD: only units in their own department.
    """
    roles = _get_user_roles()
    is_sm = "System Manager" in roles
    is_hod = "KRCS HOD" in roles
    if not is_sm and not is_hod:
        frappe.throw(_("Only System Managers or HODs can delete units."), frappe.PermissionError)
    if not is_sm and is_hod:
        own_dept = _get_current_user_department()
        unit_dept = frappe.db.get_value("Unit", name, "department")
        if not own_dept or unit_dept != own_dept:
            return {"success": False, "message": "You can only delete units in your own department."}
    try:
        frappe.delete_doc("Unit", name, ignore_permissions=True)
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
def get_current_user():
    """
    Return the current user's information including their department.
    """
    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)

    department = None
    department_name = None
    if user_doc.krcs_department:
        department = user_doc.krcs_department
        department_name = frappe.db.get_value("Department", department, "department_name")

    roles = frappe.get_all(
        "Has Role",
        filters={"parent": user, "role": ["in", KRCS_ROLES]},
        pluck="role"
    )

    # Roles that can see all departments (no auto-filter on dashboard)
    GLOBAL_VIEW_ROLES = {"System Manager", "KRCS HOR", "KRCS DSG"}
    all_roles = set(frappe.get_roles(user))
    is_global_viewer = bool(all_roles & GLOBAL_VIEW_ROLES)
    is_system_manager = "System Manager" in all_roles

    return {
        "name": user,
        "full_name": user_doc.full_name,
        "email": user_doc.email,
        "department": department,
        "department_name": department_name,
        "krcs_roles": roles,
        "all_roles": list(all_roles),
        "is_global_viewer": is_global_viewer,
        "is_system_manager": is_system_manager,
    }


@frappe.whitelist()
def get_users():
    """
    Return users with their KRCS roles.
    - System Manager: all users
    - KRCS HOD / KRCS Project Manager: only users in their own department
    """
    _require_user_manager()
    roles = _get_user_roles()

    filters = {"name": ["not in", ["Guest", "Administrator"]], "user_type": "System User"}

    # Non-system-managers can only see users in their own department
    if not _is_system_manager():
        dept = _get_current_user_department()
        if dept:
            filters["krcs_department"] = dept
        else:
            # No department set — return empty list rather than expose all users
            return []

    users = frappe.get_all(
        "User",
        filters=filters,
        fields=["name", "full_name", "email", "enabled", "creation", "krcs_department"],
        order_by="full_name asc"
    )
    # Attach roles and department name to each user
    for u in users:
        u_roles = frappe.get_all(
            "Has Role",
            filters={"parent": u["name"], "role": ["in", KRCS_ROLES]},
            pluck="role"
        )
        u["krcs_roles"] = u_roles
        if u.get("krcs_department"):
            dept_name = frappe.db.get_value("Department", u["krcs_department"], "department_name")
            u["department_name"] = dept_name
        else:
            u["department_name"] = None
    return users


@frappe.whitelist()
def create_user(email, first_name, last_name="", department=None, roles=None):
    """
    Create a new System User and assign KRCS roles and department.
    System Manager: can create users in any department with any KRCS role.
    KRCS HOD: can create users only in their own department; limited role assignment.
    KRCS Project Manager: can create users only in their own department; limited role assignment.
    roles: JSON string of role names list.
    """
    _require_user_manager()
    import json
    try:
        if frappe.db.exists("User", email):
            return {"success": False, "message": f"User '{email}' already exists."}

        role_list = json.loads(roles) if isinstance(roles, str) else (roles or [])
        current_roles = _get_user_roles()

        if not _is_system_manager():
            # Enforce own-department restriction
            own_dept = _get_current_user_department()
            if not own_dept:
                return {"success": False, "message": "Your user account has no department set. Contact a System Manager."}
            department = own_dept  # Override any supplied department

            # Restrict assignable roles
            if "KRCS HOD" in current_roles:
                allowed_roles = _HOD_ASSIGNABLE_ROLES
            else:
                allowed_roles = _PM_ASSIGNABLE_ROLES
            role_list = [r for r in role_list if r in allowed_roles]
        else:
            role_list = [r for r in role_list if r in KRCS_ROLES]

        doc = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "user_type": "System User",
            "send_welcome_email": 0,
            "krcs_department": department if department else None,
            "roles": [{"role": r} for r in role_list],
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "User created.", "name": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating user"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_user(user, department=None, roles=None):
    """
    Update user's department and KRCS roles.
    roles: JSON string of role names list.
    System Manager: can update any user.
    KRCS HOD / KRCS Project Manager: can only update users in their own department.
    """
    _require_user_manager()
    import json
    try:
        role_list = json.loads(roles) if isinstance(roles, str) else (roles or [])
        current_roles = _get_user_roles()

        if not _is_system_manager():
            own_dept = _get_current_user_department()
            if not own_dept:
                return {"success": False, "message": "Your user account has no department set. Contact a System Manager."}
            # Verify the target user belongs to this department
            target_dept = frappe.db.get_value("User", user, "krcs_department")
            if target_dept != own_dept:
                return {"success": False, "message": "You can only edit users in your own department."}
            # Department cannot be changed by HOD/PM
            department = own_dept
            # Restrict assignable roles
            if "KRCS HOD" in current_roles:
                allowed_roles = _HOD_ASSIGNABLE_ROLES
            else:
                allowed_roles = _PM_ASSIGNABLE_ROLES
            role_list = [r for r in role_list if r in allowed_roles]
        else:
            role_list = [r for r in role_list if r in KRCS_ROLES]

        user_doc = frappe.get_doc("User", user)

        # Update department
        user_doc.krcs_department = department if department else None

        # Remove existing KRCS roles and replace with new list
        user_doc.roles = [r for r in user_doc.roles if r.role not in KRCS_ROLES]
        for r in role_list:
            user_doc.append("roles", {"role": r})

        user_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "User updated."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error updating user"))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_user_roles(user, roles=None):
    """
    Replace the KRCS roles for an existing user.
    roles: JSON string of role names list.
    System Manager only.
    Legacy function - use update_user instead.
    """
    return update_user(user, None, roles)


@frappe.whitelist()
def toggle_user_enabled(user, enabled):
    """
    Enable or disable a user account.
    System Manager: any user.
    KRCS HOD / KRCS Project Manager: only users in their own department.
    """
    _require_user_manager()
    try:
        if not _is_system_manager():
            own_dept = _get_current_user_department()
            target_dept = frappe.db.get_value("User", user, "krcs_department")
            if not own_dept or target_dept != own_dept:
                return {"success": False, "message": "You can only enable/disable users in your own department."}

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
    - KRCS roles list (filtered by what the current user can assign)
    - Departments list (all for System Manager; only own dept for HOD/PM)
    - Role flags: is_system_manager, is_hod, is_pm
    - user_department: the caller's department (for locking UI)
    """
    roles = _get_user_roles()
    is_sm = "System Manager" in roles
    is_hod = "KRCS HOD" in roles
    is_pm = "KRCS Project Manager" in roles

    # Determine which roles this user is allowed to assign
    if is_sm:
        assignable_roles = KRCS_ROLES
    elif is_hod:
        assignable_roles = sorted(_HOD_ASSIGNABLE_ROLES)
    elif is_pm:
        assignable_roles = sorted(_PM_ASSIGNABLE_ROLES)
    else:
        assignable_roles = []

    all_departments = frappe.get_all(
        "Department",
        fields=["name", "department_name"],
        order_by="department_name asc"
    )

    # Non-system-managers can only see their own department in the dropdown
    user_department = _get_current_user_department() if not is_sm else None
    if not is_sm and user_department:
        departments = [d for d in all_departments if d["name"] == user_department]
    else:
        departments = all_departments

    return {
        "is_system_manager": is_sm,
        "is_hod": is_hod,
        "is_pm": is_pm,
        "user_department": user_department,
        "krcs_roles": assignable_roles,
        "departments": departments,
    }
