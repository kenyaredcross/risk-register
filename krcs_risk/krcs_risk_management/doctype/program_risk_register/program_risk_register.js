// Copyright (c) 2026, KRCS and contributors
// For license information, please see license.txt

/**
 * Risk Level Matrix - matches server-side calculation
 * Overall Rating = Likelihood × Impact (scale 1-25)
 */
const RISK_LEVEL_MATRIX = [
    { min: 1,  max: 4,  label: "Low" },
    { min: 5,  max: 9,  label: "Medium" },
    { min: 10, max: 14, label: "High" },
    { min: 15, max: 25, label: "Critical" }
];

function get_risk_level(rating) {
    if (!rating) return "";
    for (let level of RISK_LEVEL_MATRIX) {
        if (rating >= level.min && rating <= level.max) return level.label;
    }
    return "";
}

function calculate_overall_rating(frm) {
    const likelihood = frm.doc.likelihood || 0;
    const impact = frm.doc.impact || 0;
    const overall_rating = likelihood * impact;
    frm.set_value('overall_rating', overall_rating);
    frm.set_value('risk_level', overall_rating ? get_risk_level(overall_rating) : '');
}

// ---------------------------------------------------------------------------
// Approval workflow helpers
// ---------------------------------------------------------------------------

function add_approval_buttons(frm, can_approve) {
    const status = frm.doc.status;

    // --- Any user: Submit for Approval (Draft or Rejected) ---
    if (status === "Draft" || status === "Rejected") {
        frm.add_custom_button(__("Submit for Approval"), function () {
            frappe.confirm(
                "Submit this risk for approval?",
                function () {
                    frappe.call({
                        method: "krcs_risk.krcs_risk_management.doctype.program_risk_register.api.submit_for_approval",
                        args: { risk_name: frm.docname },
                        callback: function (r) {
                            if (r.message && r.message.success) {
                                frappe.show_alert({ message: r.message.message, indicator: "green" });
                                frm.reload_doc();
                            } else {
                                frappe.msgprint(r.message ? r.message.message : "Error submitting for approval.");
                            }
                        }
                    });
                }
            );
        }, __("Workflow"));
    }

    // --- Any user: Request Closure (Open) ---
    if (status === "Open") {
        frm.add_custom_button(__("Request Closure"), function () {
            frappe.confirm(
                "Request closure for this risk?",
                function () {
                    frappe.call({
                        method: "krcs_risk.krcs_risk_management.doctype.program_risk_register.api.request_close",
                        args: { risk_name: frm.docname },
                        callback: function (r) {
                            if (r.message && r.message.success) {
                                frappe.show_alert({ message: r.message.message, indicator: "green" });
                                frm.reload_doc();
                            } else {
                                frappe.msgprint(r.message ? r.message.message : "Error requesting closure.");
                            }
                        }
                    });
                }
            );
        }, __("Workflow"));
    }

    // --- Eligible approver only: Approve / Reject ---
    if (can_approve && (status === "Pending Approval" || status === "Pending Close Approval")) {
        frm.add_custom_button(__("Approve"), function () {
            frappe.confirm(
                `Approve this risk (${status})?`,
                function () {
                    frappe.call({
                        method: "krcs_risk.krcs_risk_management.doctype.program_risk_register.api.approve_risk",
                        args: { risk_name: frm.docname },
                        callback: function (r) {
                            if (r.message && r.message.success) {
                                frappe.show_alert({ message: r.message.message, indicator: "green" });
                                frm.reload_doc();
                            } else {
                                frappe.msgprint(r.message ? r.message.message : "Error approving.");
                            }
                        }
                    });
                }
            );
        }, __("Workflow"));

        frm.add_custom_button(__("Reject"), function () {
            frappe.prompt(
                [{ fieldname: "reason", fieldtype: "Small Text", label: "Rejection Reason", reqd: 1 }],
                function (values) {
                    frappe.call({
                        method: "krcs_risk.krcs_risk_management.doctype.program_risk_register.api.reject_risk",
                        args: { risk_name: frm.docname, reason: values.reason },
                        callback: function (r) {
                            if (r.message && r.message.success) {
                                frappe.show_alert({ message: r.message.message, indicator: "orange" });
                                frm.reload_doc();
                            } else {
                                frappe.msgprint(r.message ? r.message.message : "Error rejecting.");
                            }
                        }
                    });
                },
                __("Reject Risk"),
                __("Reject")
            );
        }, __("Workflow"));
    }
}

// ---------------------------------------------------------------------------
// Form events
// ---------------------------------------------------------------------------

frappe.ui.form.on("Program Risk Register", {
    refresh(frm) {
        if (frm.doc.likelihood || frm.doc.impact) {
            calculate_overall_rating(frm);
        }

        // Make status field visually read-only (it is driven by workflow actions)
        frm.set_df_property("status", "read_only", 1);

        // Fetch per-risk approval eligibility, then render workflow buttons
        frappe.call({
            method: "krcs_risk.krcs_risk_management.doctype.program_risk_register.api.can_approve_risk",
            args: { risk_name: frm.docname },
            callback: function (r) {
                const can_approve = r.message ? r.message.can_approve : false;
                add_approval_buttons(frm, can_approve);

                // Lock form fields for non-approvers when status is pending/closed
                const locked = ["Pending Approval", "Pending Close Approval", "Closed"];
                if (locked.includes(frm.doc.status) && !can_approve) {
                    frm.disable_form();
                }
            }
        });
    },

    likelihood(frm) {
        calculate_overall_rating(frm);
    },

    impact(frm) {
        calculate_overall_rating(frm);
    }
});
