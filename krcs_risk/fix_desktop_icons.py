import frappe

def fix_icons():
    """Remove app field from desktop icons to prevent permission check errors"""

    # Update all desktop icons to remove app field
    frappe.db.sql("UPDATE `tabDesktop Icon` SET app = NULL WHERE app IS NOT NULL")
    frappe.db.commit()

    # Verify the update
    icons = frappe.db.sql("""
        SELECT name, label, app, link_type
        FROM `tabDesktop Icon`
    """, as_dict=True)

    print(f"Fixed {len(icons)} desktop icons:\n")
    for icon in icons:
        print(f"  - {icon.label}: app={icon.app}, link_type={icon.link_type}")

    return {"total": len(icons)}
