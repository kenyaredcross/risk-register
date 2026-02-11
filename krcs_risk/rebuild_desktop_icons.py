import frappe

def rebuild_all_icons():
    """Rebuild all desktop icons from workspaces without affecting DocTypes"""

    # Get all public workspaces
    workspaces = frappe.get_all("Workspace",
                                 filters={"public": 1, "is_hidden": 0},
                                 fields=["name", "label", "icon", "module"])

    print(f"Found {len(workspaces)} public workspaces\n")
    print("Rebuilding desktop icons...\n")

    created = 0
    updated = 0
    skipped = 0

    for ws in workspaces:
        sidebar_name = ws.module or ws.name

        # Ensure workspace sidebar exists
        if not frappe.db.exists("Workspace Sidebar", sidebar_name):
            try:
                sidebar = frappe.new_doc("Workspace Sidebar")
                sidebar.title = sidebar_name
                sidebar.module = ws.module
                sidebar.insert(ignore_permissions=True, ignore_if_duplicate=True)
                print(f"  Created sidebar: {sidebar_name}")
            except Exception as e:
                print(f"  ⚠ Sidebar error for {sidebar_name}: {str(e)}")

        # Check if desktop icon exists
        existing = frappe.db.exists("Desktop Icon", {"label": ws.label})

        if existing:
            # Update existing icon
            try:
                icon = frappe.get_doc("Desktop Icon", existing)
                icon.link = sidebar_name
                icon.link_type = "Workspace Sidebar"
                icon.icon = ws.icon or "folder"
                icon.app = None  # Clear app field to avoid permission issues
                icon.save(ignore_permissions=True)
                updated += 1
                print(f"  ✓ Updated: {ws.label}")
            except Exception as e:
                print(f"  ⚠ Update failed for {ws.label}: {str(e)}")
                skipped += 1
        else:
            # Create new icon
            try:
                icon = frappe.new_doc("Desktop Icon")
                icon.label = ws.label
                icon.link = sidebar_name
                icon.link_type = "Workspace Sidebar"
                icon.icon = ws.icon or "folder"
                icon.standard = 1
                icon.app = None  # No app field
                icon.insert(ignore_permissions=True, ignore_if_duplicate=True)
                created += 1
                print(f"  ✓ Created: {ws.label}")
            except Exception as e:
                print(f"  ⚠ Create failed for {ws.label}: {str(e)}")
                skipped += 1

    frappe.db.commit()

    total = frappe.db.count("Desktop Icon")

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Created: {created}")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Total Desktop Icons: {total}")
    print(f"{'='*60}")

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "total": total
    }
