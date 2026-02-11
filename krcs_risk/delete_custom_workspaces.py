import frappe

def delete_custom():
    """Delete all custom (non-standard) workspaces"""

    # Get all workspaces
    all_workspaces = frappe.get_all("Workspace", fields=["name", "module", "title"])

    print(f"Found {len(all_workspaces)} total workspaces\n")
    print("Analyzing workspaces...\n")

    # Standard Frappe modules to keep
    standard_modules = [
        "Core",
        "Website",
        "Integrations",
        "Email",
        "Printing",
        "Automation",
        "Desk"
    ]

    deleted = 0
    kept = 0

    for ws in all_workspaces:
        module = ws.module or ""

        # Keep standard Frappe workspaces
        if module in standard_modules:
            kept += 1
            print(f"  ✓ Kept (standard): {ws.name} ({module})")
        else:
            # Delete custom workspace
            try:
                frappe.delete_doc("Workspace", ws.name, ignore_permissions=True, force=True)
                deleted += 1
                print(f"  ✗ Deleted (custom): {ws.name} ({module})")
            except Exception as e:
                print(f"  ⚠ Failed to delete {ws.name}: {str(e)}")

    frappe.db.commit()

    remaining = frappe.db.count("Workspace")

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Deleted: {deleted}")
    print(f"  Kept: {kept}")
    print(f"  Remaining: {remaining}")
    print(f"{'='*60}")

    return {"deleted": deleted, "kept": kept, "remaining": remaining}
