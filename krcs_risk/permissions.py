import frappe


def check_app_permission():
	"""
	Check if the current user should have access to the Risk Dashboard app.
	Only users with KRCS roles should see this app on the apps screen.
	"""
	if frappe.session.user == "Administrator":
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

	# Get user's roles
	user_roles = frappe.get_roles(frappe.session.user)

	# Check if user has any KRCS role
	return bool(set(user_roles) & krcs_roles)
