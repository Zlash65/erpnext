# Copyright (c) 2018, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from frappe.model.rename_doc import rename_doc
import frappe

def execute():
    frappe.reload_doc('projects', 'doctype', 'timesheet')
    frappe.reload_doc('stock', 'doctype', 'stock_entry')

    rename_doc('DocType', 'Production Order', 'Work Order', force=True)
    frappe.reload_doc('manufacturing', 'doctype', 'work_order')

    rename_doc('DocType', 'Production Order Item', 'Work Order Item', force=True)
    frappe.reload_doc('manufacturing', 'doctype', 'work_order_item')

    rename_doc('DocType', 'Production Order Operation', 'Work Order Operation', force=True)
    frappe.reload_doc('manufacturing', 'doctype', 'work_order_operation')