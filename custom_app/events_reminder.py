import frappe
from frappe.utils import now_datetime,add_to_date,get_datetime

def trigger_events():
	current_dt =now_datetime()

	notification_conditions = {
		"7 days alert": add_to_date(current_dt, weeks = 1, as_string = False),
		"1 day alert": add_to_date(current_dt, days = 1, as_string = False),
		"60 min alert": add_to_date(current_dt, hours = 1, as_string = False)
}

	scheduled_events = frappe.get_all('Event',filters={"custom_enable_reminders":1},fields=['name','event_date','titls'])

	for scheduled_event in scheduled_events:
		event_start_time = get_datetime(scheduled_event["event_date"])

		for alert, notify in notification_conditions.items():
			if notify <= event_start_time < add_to_date(notify,seconds=60,as_string = False):
				send_alert_to_invite(scheduled_event,alert)
				break

def send_alert_to_invite(scheduled_event,alert):
	invites = frappe.get_all("Event Participants",filters={'parent':scheduled_event['name']},
				fields=['reference_document_type','email','reference_name'])

	for invite in invites:
		message_content = f"""Reminder"""
		if invite['email']:
			frappe.sendmail(recipients = invite['email'],
					subject= f"notification:{scheduled_event['title']}",
					message = message_content,
					)
