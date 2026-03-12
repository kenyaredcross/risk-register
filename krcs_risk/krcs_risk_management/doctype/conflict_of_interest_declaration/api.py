# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime


@frappe.whitelist()
def get_employees():
	"""
	Get list of all active employees for dropdown
	"""
	employees = frappe.get_all(
		"Employee",
		filters={"status": "Active"},
		fields=["name", "employee_name", "department", "designation", "user_id"],
		order_by="employee_name asc"
	)
	return employees


@frappe.whitelist()
def create_declaration(data):
	"""
	Create a new COI declaration from Vue frontend
	"""
	import json
	if isinstance(data, str):
		data = json.loads(data)

	# Create new document
	doc = frappe.new_doc("Conflict of Interest Declaration")

	# Set fields from data
	doc.employee = data.get("employee")
	doc.declaration_type = data.get("declaration_type")
	doc.declaration_date = data.get("declaration_date")

	# Financial interests
	doc.has_financial_interests = data.get("has_financial_interests")
	if data.get("financial_interests_description"):
		doc.financial_interests_description = data.get("financial_interests_description")

	# Personal relationships
	doc.has_personal_relationships = data.get("has_personal_relationships")
	if data.get("personal_relationships_description"):
		doc.personal_relationships_description = data.get("personal_relationships_description")

	# Supervisory roles
	doc.has_supervisory_roles = data.get("has_supervisory_roles")
	if data.get("supervisory_roles_description"):
		doc.supervisory_roles_description = data.get("supervisory_roles_description")

	# Other roles
	doc.has_other_roles = data.get("has_other_roles")
	if data.get("other_roles_description"):
		doc.other_roles_description = data.get("other_roles_description")

	# Public office
	doc.plans_public_office = data.get("plans_public_office")
	if data.get("public_office_description"):
		doc.public_office_description = data.get("public_office_description")

	# Set status
	doc.status = data.get("status", "Draft")

	# Save
	doc.insert()

	# If submitting directly, update status
	if data.get("submit"):
		doc.status = "Submitted"
		doc.submitted_date = now_datetime()
		doc.save()

	frappe.db.commit()

	return {
		"success": True,
		"message": "Declaration created successfully",
		"name": doc.name
	}


@frappe.whitelist()
def update_declaration(name, data):
	"""
	Update an existing declaration
	"""
	import json
	if isinstance(data, str):
		data = json.loads(data)

	doc = frappe.get_doc("Conflict of Interest Declaration", name)

	# Check permissions
	if not frappe.has_permission("Conflict of Interest Declaration", "write", doc=doc):
		frappe.throw("You do not have permission to update this declaration")

	# Update fields
	if "declaration_type" in data:
		doc.declaration_type = data["declaration_type"]

	# Financial interests
	if "has_financial_interests" in data:
		doc.has_financial_interests = data["has_financial_interests"]
	if "financial_interests_description" in data:
		doc.financial_interests_description = data["financial_interests_description"]

	# Personal relationships
	if "has_personal_relationships" in data:
		doc.has_personal_relationships = data["has_personal_relationships"]
	if "personal_relationships_description" in data:
		doc.personal_relationships_description = data["personal_relationships_description"]

	# Supervisory roles
	if "has_supervisory_roles" in data:
		doc.has_supervisory_roles = data["has_supervisory_roles"]
	if "supervisory_roles_description" in data:
		doc.supervisory_roles_description = data["supervisory_roles_description"]

	# Other roles
	if "has_other_roles" in data:
		doc.has_other_roles = data["has_other_roles"]
	if "other_roles_description" in data:
		doc.other_roles_description = data["other_roles_description"]

	# Public office
	if "plans_public_office" in data:
		doc.plans_public_office = data["plans_public_office"]
	if "public_office_description" in data:
		doc.public_office_description = data["public_office_description"]

	doc.save()

	# If submitting, update status
	if data.get("submit"):
		doc.status = "Submitted"
		doc.submitted_date = now_datetime()
		doc.save()

	frappe.db.commit()

	return {
		"success": True,
		"message": "Declaration updated successfully"
	}


@frappe.whitelist()
def get_declaration(name):
	"""
	Get a specific declaration by name
	"""
	doc = frappe.get_doc("Conflict of Interest Declaration", name)

	# Check permissions
	if not frappe.has_permission("Conflict of Interest Declaration", "read", doc=doc):
		frappe.throw("You do not have permission to view this declaration")

	return doc.as_dict()


@frappe.whitelist()
def get_user_employee():
	"""
	Get the employee record linked to the current user
	"""
	user = frappe.session.user

	employee = frappe.db.get_value(
		"Employee",
		{"user_id": user, "status": "Active"},
		["name", "employee_name", "department", "designation", "user_id"],
		as_dict=True
	)

	return employee or None


@frappe.whitelist()
def get_declaration_stats():
	"""
	Get statistics for declarations (for dashboard)
	"""
	user = frappe.session.user
	user_roles = frappe.get_roles()

	stats = {
		"my_declarations": 0,
		"pending_submissions": 0,
		"pending_reviews": 0,
		"approved": 0,
		"rejected": 0
	}

	# Get employee for current user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

	if employee:
		# My declarations
		stats["my_declarations"] = frappe.db.count(
			"Conflict of Interest Declaration",
			{"employee": employee}
		)

		# My pending submissions (drafts)
		stats["pending_submissions"] = frappe.db.count(
			"Conflict of Interest Declaration",
			{"employee": employee, "status": "Draft"}
		)

		# My approved
		stats["approved"] = frappe.db.count(
			"Conflict of Interest Declaration",
			{"employee": employee, "status": "Approved"}
		)

		# My rejected
		stats["rejected"] = frappe.db.count(
			"Conflict of Interest Declaration",
			{"employee": employee, "status": "Rejected"}
		)

	# Pending reviews (if user is HOD/HOR)
	if "KRCS HOD" in user_roles or "KRCS HOR" in user_roles or "System Manager" in user_roles:
		stats["pending_reviews"] = frappe.db.count(
			"Conflict of Interest Declaration",
			{"status": "Submitted"}
		)

	return stats


@frappe.whitelist()
def get_all_declarations(filters=None):
	"""
	Get all declarations with optional filters
	For employees: only their own declarations
	For HOD/HOR: all declarations
	"""
	import json
	if isinstance(filters, str):
		filters = json.loads(filters) if filters else {}

	user = frappe.session.user
	user_roles = frappe.get_roles()

	# Build filters
	query_filters = filters or {}

	# If not HOD/HOR, only show user's own declarations
	if not ("KRCS HOD" in user_roles or "KRCS HOR" in user_roles or "System Manager" in user_roles):
		employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
		if employee:
			query_filters["employee"] = employee
		else:
			return []

	# Get declarations
	declarations = frappe.get_all(
		"Conflict of Interest Declaration",
		filters=query_filters,
		fields=[
			"name", "employee", "employee_name", "department", "designation",
			"declaration_type", "declaration_date", "status", "submitted_date",
			"approved_by", "approval_date", "reviewed_by", "review_date"
		],
		order_by="declaration_date desc, modified desc"
	)

	return declarations
