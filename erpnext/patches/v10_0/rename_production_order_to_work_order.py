# Copyright (c) 2017, Frappe and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
	frappe.reload_doc('manufacturing', 'doctype', 'work_order')
	frappe.reload_doc('manufacturing', 'doctype', 'work_order_item')
	frappe.reload_doc('manufacturing', 'doctype', 'work_order_operation')

	frappe.db.sql(""" insert into `tabWork Order Item` (name, item_code, source_warehouse, creation,
			item_name, description, required_qty, transferred_qty, modified, modified_by, owner,
			available_qty_at_source_warehouse, available_qty_at_wip_warehouse, docstatus,
			parent, parentfield, parenttype, idx)
			select name, item_code, source_warehouse, creation, item_name, description, required_qty,
			transferred_qty, modified, modified_by, owner, available_qty_at_source_warehouse,
			available_qty_at_wip_warehouse, docstatus, parent, parentfield, parenttype, idx
			from `tabProduction Order Item`""")

	frappe.db.sql(""" insert into `tabWork Order Operation` (name, creation, operation, bom,
			description, completed_qty, status, workstation, modified,
			planned_start_time, planned_end_time ,time_in_mins,hour_rate, modified_by, owner, docstatus,
			planned_operating_cost, actual_start_time, actual_end_time, parent, parentfield, 
			actual_operation_time, actual_operating_cost, idx)
			select name, creation, operation, bom,
			description, completed_qty, status, workstation, modified,
			planned_start_time, planned_end_time ,time_in_mins,hour_rate, modified_by, owner, docstatus,
			planned_operating_cost, actual_start_time, actual_end_time, parent, parentfield, 
			actual_operation_time, actual_operating_cost, idx
			from `tabProduction Order Operation`""")

	frappe.db.sql(""" update `tabWork Order Item` set parenttype='Work order'""")
	frappe.db.sql(""" update `tabWork Order Operation` set parenttype='Work order'""")

	frappe.db.sql(""" insert into `tabWork Order` (name, creation, modified, modified_by, status,
			production_item, bom_no, use_multi_level_bom, qty, produced_qty, owner, docstatus,
			material_transferred_for_manufacturing, sales_order,project, parent, parentfield,
			skip_transfer, wip_warehouse, fg_warehouse, parenttype, idx,
			scrap_warehouse, planned_start_date, actual_start_date, planned_end_date,
			actual_end_date, expected_delivery_date,
			planned_operating_cost, actual_operating_cost, additional_operating_cost,
			total_operating_cost, description, stock_uom, company,
			material_request, material_request_item, sales_order_item, amended_from)
			select
			name, creation, modified, modified_by, status,
			production_item, bom_no, use_multi_level_bom, qty, produced_qty, owner, docstatus,
			material_transferred_for_manufacturing, sales_order,project, parent, parentfield,
			skip_transfer, wip_warehouse, fg_warehouse, parenttype, idx,
			scrap_warehouse, planned_start_date, actual_start_date, planned_end_date,
			actual_end_date, expected_delivery_date,
			planned_operating_cost, actual_operating_cost, additional_operating_cost,
			total_operating_cost, description, stock_uom, company,
			material_request, material_request_item, sales_order_item, amended_from
			from `tabProduction Order`""")
