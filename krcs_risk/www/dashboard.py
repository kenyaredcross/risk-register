# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe

ALLOWED_ROLES = {
	"Administrator",
	"System Manager",
	"KRCS HOR",
	"KRCS DSG",
	"KRCS HOD",
	"KRCS Project Manager",
	"KRCS RPC",
	"KRCS Finance Officer",
	"KRCS Procurement Manager",
	"KRCS Logistics Manager",
	"KRCS HR Manager",
	"KRCS Audit",
}

def get_context(context):
	"""
	Context for the Risk Management Dashboard web page.
	Only Administrator and users with a KRCS role may access this page.
	"""
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	user_roles = set(frappe.get_roles(frappe.session.user))
	if not (user_roles & ALLOWED_ROLES):
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	context.no_cache = 1
	context.title = "Risk Management Dashboard"
	context.show_sidebar = False
	return context
