import frappe


def check_app_permission():
	"""
	Check if the current user should have access to the Risk Dashboard app.
	- KRCS roles have access to Risk Management features
	- All active employees have access to COI Declaration features
	- System Manager and KRCS Audit have full access
	"""
	if frappe.session.user == "Administrator":
		return True

	# Get user's roles
	user_roles = frappe.get_roles(frappe.session.user)

	# System Manager and KRCS Audit always have access
	if "System Manager" in user_roles or "KRCS Audit" in user_roles:
		return True

	# KRCS roles that should have access to the Risk Dashboard
	krcs_roles = {
		"KRCS HOR",
		"KRCS DSG",
		"KRCS HOD",
		"KRCS Project Manager",
		"KRCS RPC",
		"KRCS Finance Officer",
		"KRCS Procurement Manager",
		"KRCS Logistics Manager",
		"KRCS HR Manager",
	}

	# Check if user has any KRCS role
	if bool(set(user_roles) & krcs_roles):
		return True

	# Check if user is an active employee (for COI declarations)
	employee = frappe.db.get_value(
		"Employee",
		{"user_id": frappe.session.user, "status": "Active"},
		"name"
	)

	# If user has an active employee record, grant access
	return bool(employee)
