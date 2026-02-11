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

/**
 * Get risk level label based on overall rating
 * @param {number} rating - Overall rating (likelihood × impact)
 * @returns {string} Risk level label
 */
function get_risk_level(rating) {
    if (!rating) return "";

    for (let level of RISK_LEVEL_MATRIX) {
        if (rating >= level.min && rating <= level.max) {
            return level.label;
        }
    }
    return "";
}

/**
 * Calculate overall rating and risk level
 * @param {object} frm - Frappe form object
 */
function calculate_overall_rating(frm) {
    const likelihood = frm.doc.likelihood || 0;
    const impact = frm.doc.impact || 0;

    // Calculate overall rating: likelihood × impact
    const overall_rating = likelihood * impact;

    // Set the calculated values
    frm.set_value('overall_rating', overall_rating);

    // Calculate and set risk level
    if (overall_rating) {
        const risk_level = get_risk_level(overall_rating);
        frm.set_value('risk_level', risk_level);
    } else {
        frm.set_value('risk_level', '');
    }
}

frappe.ui.form.on("Program Risk Register", {
    refresh(frm) {
        // Calculate on form load in case values are present
        if (frm.doc.likelihood || frm.doc.impact) {
            calculate_overall_rating(frm);
        }
    },

    likelihood(frm) {
        // Recalculate when likelihood changes
        calculate_overall_rating(frm);
    },

    impact(frm) {
        // Recalculate when impact changes
        calculate_overall_rating(frm);
    }
});
