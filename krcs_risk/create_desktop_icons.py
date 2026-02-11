import frappe

def create_all_icons():
    """Create desktop icons for all workspaces"""

    icons_to_create = [
        {"label": "Risk Managemnt Wksp", "module": "KRCS Risk Management", "icon": "archive"},
        {"label": "System", "module": "Core", "icon": "settings"},
        {"label": "Welcome Workspace", "module": "Core", "icon": "home"},
        {"label": "Build", "module": "Core", "icon": "tool"},
        {"label": "Integrations", "module": "Integrations", "icon": "shuffle"},
    ]

    created = 0
    skipped = 0

    for ws_data in icons_to_create:
        # Ensure sidebar exists
        if not frappe.db.exists("Workspace Sidebar", ws_data["module"]):
            sidebar = frappe.new_doc("Workspace Sidebar")
            sidebar.title = ws_data["module"]
            sidebar.module = ws_data["module"]
            sidebar.insert(ignore_permissions=True, ignore_if_duplicate=True)

        # Check if icon exists
        if frappe.db.exists("Desktop Icon", {"label": ws_data["label"]}):
            print(f"  Skip: {ws_data['label']}")
            skipped += 1
            continue

        # Create icon
        icon = frappe.new_doc("Desktop Icon")
        icon.label = ws_data["label"]
        icon.link = ws_data["module"]
        icon.link_type = "Workspace Sidebar"
        icon.icon = ws_data["icon"]
        icon.standard = 1
        icon.insert(ignore_permissions=True, ignore_if_duplicate=True)
        print(f"  ✓ Created: {ws_data['label']}")
        created += 1

    frappe.db.commit()

    total = frappe.db.count("Desktop Icon")
    print(f"\n{'='*50}")
    print(f"Created: {created}, Skipped: {skipped}")
    print(f"Total Desktop Icons: {total}")

    return {"created": created, "skipped": skipped, "total": total}
