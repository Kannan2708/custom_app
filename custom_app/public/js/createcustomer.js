frappe.listview_settings['Lead'] = {
    onload: function (listview) {
        listview.page.add_action_item(__('Bulk Convert to Customer'), function () {
            const selected_leads = listview.get_checked_items(); // Get selected leads
            if (selected_leads.length === 0) {
                frappe.msgprint(__('Please select at least one Lead.'));
                return;
            }

            frappe.call({
                method: 'custom_app.createcustomer.bulk_convert_leads_to_customers',
                args: {
                    leads: JSON.stringify(selected_leads.map(d => d.name)) // Pass the names as JSON
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint(__('Leads have been successfully converted to customers.'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
