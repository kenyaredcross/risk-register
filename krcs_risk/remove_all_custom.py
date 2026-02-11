import frappe

def remove_all():
    """Remove all custom workspaces, workspace sidebars, and related desktop icons"""

    print("Removing all custom workspaces and related items...\n")

    deleted_ws = 0
    deleted_sidebar = 0
    deleted_icons = 0

    # 1. Delete custom workspaces
    print("1. Deleting custom workspaces...")
    standard_modules = ["Core", "Website", "Integrations", "Email", "Printing", "Automation", "Desk"]
    workspaces = frappe.get_all("Workspace", fields=["name", "module"])

    for ws in workspaces:
        if ws.module not in standard_modules:
            try:
                frappe.delete_doc("Workspace", ws.name, ignore_permissions=True, force=True)
                deleted_ws += 1
                print(f"  ✗ Deleted workspace: {ws.name}")
            except Exception as e:
                print(f"  ⚠ Failed to delete workspace {ws.name}: {str(e)}")

    # 2. Delete custom workspace sidebars
    print("\n2. Deleting custom workspace sidebars...")
    sidebars = frappe.get_all("Workspace Sidebar", fields=["name", "module"])

    for sidebar in sidebars:
        if sidebar.module not in standard_modules:
            try:
                frappe.delete_doc("Workspace Sidebar", sidebar.name, ignore_permissions=True, force=True)
                deleted_sidebar += 1
                print(f"  ✗ Deleted sidebar: {sidebar.name}")
            except Exception as e:
                print(f"  ⚠ Failed to delete sidebar {sidebar.name}: {str(e)}")

    # 3. Delete related desktop icons
    print("\n3. Deleting custom workspace desktop icons...")
    icons = frappe.db.sql("""
        SELECT name, label, link
        FROM `tabDesktop Icon`
        WHERE link_type = 'Workspace Sidebar'
        AND link NOT IN (%s)
    """ % ", ".join([f"'{m}'" for m in standard_modules]), as_dict=True)

    for icon in icons:
        try:
            frappe.delete_doc("Desktop Icon", icon.name, ignore_permissions=True, force=True)
            deleted_icons += 1
            print(f"  ✗ Deleted icon: {icon.label}")
        except Exception as e:
            print(f"  ⚠ Failed to delete icon {icon.label}: {str(e)}")

    frappe.db.commit()

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Deleted workspaces: {deleted_ws}")
    print(f"  Deleted sidebars: {deleted_sidebar}")
    print(f"  Deleted icons: {deleted_icons}")
    print(f"\n  Remaining workspaces: {frappe.db.count('Workspace')}")
    print(f"  Remaining desktop icons: {frappe.db.count('Desktop Icon')}")
    print(f"{'='*60}")

    return {
        "deleted_workspaces": deleted_ws,
        "deleted_sidebars": deleted_sidebar,
        "deleted_icons": deleted_icons
    }
