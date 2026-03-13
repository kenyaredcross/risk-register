# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ConflictofInterestDeclaration(Document):
	def validate(self):
		"""Validate the declaration before saving"""
		# Ensure employee field is set
		if not self.employee:
			frappe.throw("Employee is required")

		# Auto-set user_id if not set
		if not self.user_id and self.employee:
			employee_doc = frappe.get_doc("Employee", self.employee)
			if employee_doc.user_id:
				self.user_id = employee_doc.user_id

	def before_save(self):
		"""Actions before saving the document"""
		# Set submitted_date when status changes to Submitted
		if self.status == "Submitted" and not self.submitted_date:
			self.submitted_date = now_datetime()

	def on_submit(self):
		"""Custom submit logic"""
		self.status = "Submitted"
		self.submitted_date = now_datetime()

	def on_update(self):
		"""Actions after the document is saved"""
		# Track status changes
		if self.has_value_changed("status"):
			self.add_comment("Info", f"Status changed to {self.status}")


@frappe.whitelist()
def get_employee_details(employee):
	"""
	Fetch employee details for auto-population
	"""
	if not employee:
		return {}

	employee_doc = frappe.get_doc("Employee", employee)

	return {
		"employee_name": employee_doc.employee_name,
		"user_id": employee_doc.user_id,
		"department": employee_doc.department,
		"designation": employee_doc.designation
	}


@frappe.whitelist()
def submit_declaration(name):
	"""
	Submit a declaration (change status from Draft to Submitted)
	"""
	doc = frappe.get_doc("Conflict of Interest Declaration", name)

	# Check permissions
	if not frappe.has_permission("Conflict of Interest Declaration", "write", doc=doc):
		frappe.throw("You do not have permission to submit this declaration")

	# Validate all required fields are filled
	doc.validate()

	# Update status
	doc.status = "Submitted"
	doc.submitted_date = now_datetime()
	doc.save()

	frappe.msgprint("Declaration submitted successfully")

	return {"success": True, "message": "Declaration submitted successfully"}


@frappe.whitelist()
def approve_declaration(name, comments=None):
	"""
	Approve a declaration
	"""
	doc = frappe.get_doc("Conflict of Interest Declaration", name)

	# Check if user has permission to approve
	user_roles = frappe.get_roles()
	if not ("KRCS HOD" in user_roles or "KRCS HOR" in user_roles or "System Manager" in user_roles):
		frappe.throw("You do not have permission to approve declarations")

	# Update approval fields
	doc.status = "Approved"
	doc.approved_by = frappe.session.user
	doc.approval_date = now_datetime()
	if comments:
		doc.review_comments = comments

	doc.save()

	frappe.msgprint("Declaration approved successfully")

	return {"success": True, "message": "Declaration approved successfully"}


@frappe.whitelist()
def reject_declaration(name, comments):
	"""
	Reject a declaration
	"""
	if not comments:
		frappe.throw("Please provide rejection comments")

	doc = frappe.get_doc("Conflict of Interest Declaration", name)

	# Check if user has permission to reject
	user_roles = frappe.get_roles()
	if not ("KRCS HOD" in user_roles or "KRCS HOR" in user_roles or "System Manager" in user_roles):
		frappe.throw("You do not have permission to reject declarations")

	# Update rejection fields
	doc.status = "Rejected"
	doc.reviewed_by = frappe.session.user
	doc.review_date = now_datetime()
	doc.review_comments = comments

	doc.save()

	frappe.msgprint("Declaration rejected")

	return {"success": True, "message": "Declaration rejected"}


@frappe.whitelist()
def get_my_declarations():
	"""
	Get all declarations for the current user's employee record
	"""
	user = frappe.session.user

	# Find employee linked to this user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

	if not employee:
		return []

	# Get all declarations for this employee
	declarations = frappe.get_all(
		"Conflict of Interest Declaration",
		filters={"employee": employee},
		fields=["name", "employee_name", "declaration_type", "declaration_date",
		        "status", "submitted_date", "approval_date"],
		order_by="declaration_date desc"
	)

	return declarations


@frappe.whitelist()
def get_pending_reviews():
	"""
	Get all declarations pending review (for HOD/HOR)
	"""
	user_roles = frappe.get_roles()

	if not ("KRCS HOD" in user_roles or "KRCS HOR" in user_roles or "System Manager" in user_roles):
		frappe.throw("You do not have permission to access pending reviews")

	# Get all submitted declarations
	declarations = frappe.get_all(
		"Conflict of Interest Declaration",
		filters={"status": "Submitted"},
		fields=["name", "employee", "employee_name", "department", "declaration_type",
		        "declaration_date", "submitted_date"],
		order_by="submitted_date asc"
	)

	return declarations
