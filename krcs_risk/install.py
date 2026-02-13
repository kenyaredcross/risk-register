import frappe

def after_migrate():
    """Create custom fields after migration"""
    create_user_department_field()

def create_user_department_field():
    """Create custom field for User department"""
    if not frappe.db.exists("Custom Field", "User-krcs_department"):
        doc = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "User",
            "fieldname": "krcs_department",
            "fieldtype": "Link",
            "options": "Department",
            "label": "Department",
            "insert_after": "bio",
            "in_standard_filter": 1
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Created custom field: User-krcs_department")
