# Copyright (c) 2026, KRCS and contributors
# For license information, please see license.txt

import frappe

def get_context(context):
    """
    Context for the Risk Management Dashboard web page.
    Authentication is handled entirely in the Vue app via Frappe session API.
    """
    context.no_cache = 1
    context.title = "Risk Management Dashboard"
    context.show_sidebar = False
    # Pass current user so Vue can bootstrap auth state without an extra API call
    context.frappe_user = frappe.session.user or "Guest"
    context.frappe_full_name = frappe.utils.get_fullname(frappe.session.user) if frappe.session.user and frappe.session.user != "Guest" else ""
    return context
