// Copyright (c) 2025, Pavithra M R and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inventory Optimization Rules', {
    refresh(frm) {
        frm.add_custom_button('Calculate Optimal Distribution1', () => {
            frappe.call({
                method: 'icm.inventory_control_management.api.calculate_optimal_distribution',
                args: {
                    docname: frm.doc.name
                },
                callback: () => {
                    frm.reload_doc();
                }
            });
        });
    }
});

frappe.ui.form.on('Inventory Optimization Rules', {
    refresh: function (frm) {
/*        frm.add_custom_button(__('transfer'), function () {
            frappe.call({
                method: 'icm.inventory_control_management.api.generate_transfer_orders_from_rules',
                args: {
                    docname: frm.doc.name
                },
                callback: function () {
                    frm.reload_doc();
                }
            });
        }, __('Actions'));*/
        frm.add_custom_button(__('Run Forecast'), function () {
            frappe.call({
                method: 'icm.inventory_control_management.api.calculate_seasonal_forecast',
                args: {
                    docname: frm.doc.name
                },
                callback: function () {
                    frm.reload_doc();
                }
            });
        }, __('Actions'));
    }
});
