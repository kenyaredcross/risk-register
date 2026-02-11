# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe

def get_context(context):
    """
    Context for the Risk Management Dashboard web page
    """
    context.no_cache = 1

    # Check if user is logged in
    if frappe.session.user == "Guest":
        frappe.throw("Please login to access the dashboard", frappe.PermissionError)

    # Set page title and meta
    context.title = "Risk Management Dashboard"
    context.show_sidebar = False

    return context
