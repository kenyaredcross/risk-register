import frappe

def reset_all_config():
    """Reset all workspace configuration to defaults without touching DocTypes"""

    print("="*70)
    print("RESETTING FRAPPE CONFIGURATION (DocTypes will NOT be affected)")
    print("="*70)

    stats = {
        "deleted_workspaces": 0,
        "deleted_sidebars": 0,
        "deleted_icons": 0,
        "deleted_number_cards": 0
    }

    # 1. Delete ALL workspaces
    print("\n1. Deleting all workspaces...")
    workspaces = frappe.get_all("Workspace", fields=["name"])
    for ws in workspaces:
        try:
            frappe.delete_doc("Workspace", ws.name, ignore_permissions=True, force=True)
            stats["deleted_workspaces"] += 1
            print(f"  ✗ Deleted: {ws.name}")
        except Exception as e:
            print(f"  ⚠ Failed: {ws.name} - {str(e)}")

    # 2. Delete ALL workspace sidebars
    print("\n2. Deleting all workspace sidebars...")
    sidebars = frappe.get_all("Workspace Sidebar", fields=["name"])
    for sidebar in sidebars:
        try:
            frappe.delete_doc("Workspace Sidebar", sidebar.name, ignore_permissions=True, force=True)
            stats["deleted_sidebars"] += 1
            print(f"  ✗ Deleted: {sidebar.name}")
        except Exception as e:
            print(f"  ⚠ Failed: {sidebar.name} - {str(e)}")

    # 3. Delete ALL desktop icons
    print("\n3. Deleting all desktop icons...")
    icons = frappe.get_all("Desktop Icon", fields=["name", "label"])
    for icon in icons:
        try:
            frappe.delete_doc("Desktop Icon", icon.name, ignore_permissions=True, force=True)
            stats["deleted_icons"] += 1
            print(f"  ✗ Deleted: {icon.label}")
        except Exception as e:
            print(f"  ⚠ Failed: {icon.label} - {str(e)}")

    # 4. Delete ALL number cards
    print("\n4. Deleting all number cards...")
    cards = frappe.get_all("Number Card", fields=["name", "label"])
    for card in cards:
        try:
            frappe.delete_doc("Number Card", card.name, ignore_permissions=True, force=True)
            stats["deleted_number_cards"] += 1
            print(f"  ✗ Deleted: {card.label}")
        except Exception as e:
            print(f"  ⚠ Failed: {card.label} - {str(e)}")

    frappe.db.commit()

    print("\n" + "="*70)
    print("RESET COMPLETE")
    print("="*70)
    print(f"\nDeleted:")
    print(f"  - Workspaces: {stats['deleted_workspaces']}")
    print(f"  - Workspace Sidebars: {stats['deleted_sidebars']}")
    print(f"  - Desktop Icons: {stats['deleted_icons']}")
    print(f"  - Number Cards: {stats['deleted_number_cards']}")

    print(f"\nRemaining:")
    print(f"  - Workspaces: {frappe.db.count('Workspace')}")
    print(f"  - Desktop Icons: {frappe.db.count('Desktop Icon')}")
    print(f"  - Number Cards: {frappe.db.count('Number Card')}")

    print("\n" + "="*70)
    print("✓ ALL DOCTYPES ARE SAFE AND UNCHANGED")
    print("="*70)
    print("\nNext steps:")
    print("1. Run: bench --site risk.redcross.or.ke migrate")
    print("2. This will recreate all standard Frappe workspaces")
    print("3. Then rebuild your custom workspace from the JSON files")

    return stats
