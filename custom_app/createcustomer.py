import frappe

@frappe.whitelist()
def convert_to_customer(leads):
	import json
	leads = json.loads(leads)
	for lead in leads:
		lead = frappe.get_doc('Lead',lead)
		customer = frappe.new_doc('Customer')
		customer.customer_name = lead.company
		customer.territory = lead.territory
		customer.insert()

		lead.status = 'Converted'
		lead.save()


