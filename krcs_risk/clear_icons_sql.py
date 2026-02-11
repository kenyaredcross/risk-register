import frappe

def clear():
    """Delete all desktop icons via SQL"""
    frappe.db.sql("DELETE FROM `tabDesktop Icon`")
    frappe.db.commit()

    count = frappe.db.sql("SELECT COUNT(*) FROM `tabDesktop Icon`")[0][0]
    print(f"✓ All desktop icons deleted. Remaining: {count}")

    return {"remaining": count}
