import frappe

def list_all():
    """List all desktop icons"""
    icons = frappe.db.sql("""
        SELECT name, label, link, link_type
        FROM `tabDesktop Icon`
        ORDER BY label
    """, as_dict=True)

    print(f"\nTotal Desktop Icons: {len(icons)}\n")
    print(f"{'Label':<30} {'Link':<25} {'Type':<20}")
    print("="*75)

    for icon in icons:
        label = icon.label or "(no label)"
        link = icon.link or "(none)"
        link_type = icon.link_type or "?"
        print(f"{label:<30} {link:<25} {link_type:<20}")

    # Check for Risk Management specifically
    print("\n" + "="*75)
    risk_icons = [i for i in icons if "risk" in i.label.lower()]
    if risk_icons:
        print(f"\nFound {len(risk_icons)} Risk Management icon(s):")
        for icon in risk_icons:
            print(f"  - {icon.label} → {icon.link} ({icon.link_type})")
    else:
        print("\n⚠ No Risk Management desktop icon found!")

    return {"total": len(icons), "risk_icons": len(risk_icons)}
