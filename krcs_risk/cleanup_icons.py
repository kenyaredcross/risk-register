import frappe

def cleanup():
    """Remove broken desktop icons with no links"""

    # Get all desktop icons
    icons = frappe.db.sql("""
        SELECT name, label, link, link_type
        FROM `tabDesktop Icon`
    """, as_dict=True)

    print(f"Found {len(icons)} desktop icons\n")
    print("Cleaning up broken icons...\n")

    deleted = 0
    kept = 0

    for icon in icons:
        # Delete icons with no link (broken)
        if not icon.link or icon.link.strip() == "":
            try:
                frappe.delete_doc("Desktop Icon", icon.name, ignore_permissions=True, force=True)
                deleted += 1
                print(f"  ✗ Deleted: {icon.label} (no link)")
            except Exception as e:
                print(f"  ⚠ Failed to delete {icon.label}: {str(e)}")
        else:
            kept += 1
            print(f"  ✓ Kept: {icon.label} → {icon.link}")

    frappe.db.commit()

    remaining = frappe.db.count("Desktop Icon")

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Deleted: {deleted}")
    print(f"  Kept: {kept}")
    print(f"  Remaining: {remaining}")
    print(f"{'='*60}")

    return {"deleted": deleted, "kept": kept, "remaining": remaining}
