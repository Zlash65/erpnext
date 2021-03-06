import frappe
from frappe import _
import json

@frappe.whitelist()
def get_last_interaction(contact=None, lead=None):

	if not contact and not lead: return

	last_communication = None
	last_issue = None
	if contact:
		query_condition = ''
		values = []
		contact = frappe.get_doc('Contact', contact)
		for link in contact.links:
			if link.link_doctype == 'Customer':
				last_issue = get_last_issue_from_customer(link.link_name)
			query_condition += "(`reference_doctype`=%s AND `reference_name`=%s) OR"
			values += [link_link_doctype, link_link_name]

		if query_condition:
			# remove extra appended 'OR'
			query_condition = query_condition[:-2]
			last_communication = frappe.db.sql("""
				SELECT `name`, `content`
				FROM `tabCommunication`
				WHERE `sent_or_received`='Received'
				AND ({})
				ORDER BY `modified`
				LIMIT 1
			""".format(query_condition), values, as_dict=1)  # nosec

	if lead:
		last_communication = frappe.get_all('Communication', filters={
			'reference_doctype': 'Lead',
			'reference_name': lead,
			'sent_or_received': 'Received'
		}, fields=['name', 'content'], order_by='`creation` DESC', limit=1)

	last_communication = last_communication[0] if last_communication else None

	return {
		'last_communication': last_communication,
		'last_issue': last_issue
	}

def get_last_issue_from_customer(customer_name):
	issues = frappe.get_all('Issue', {
		'customer': customer_name
	}, ['name', 'subject', 'customer'], order_by='`creation` DESC', limit=1)

	return issues[0] if issues else None


def get_scheduled_employees_for_popup(communication_medium):
	now_time = frappe.utils.nowtime()
	weekday = frappe.utils.get_weekday()

	available_employee_groups = frappe.get_all("Communication Medium Timeslot", filters={
		'day_of_week': weekday,
		'parent': communication_medium,
		'from_time': ['<=', now_time],
		'to_time': ['>=', now_time],
	}, fields=['employee_group'])

	available_employee_groups = tuple([emp.employee_group for emp in available_employee_groups])

	employees = frappe.get_all('Employee Group Table', filters={
		'parent': ['in', available_employee_groups]
	}, fields=['user_id'])

	employee_emails = set([employee.user_id for employee in employees])

	return employee_emails
