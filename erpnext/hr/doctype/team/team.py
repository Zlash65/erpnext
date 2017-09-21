# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

class Team(Document):
	def autoname(self):
		""" Set name as Team Name """
		self.name = self.team_name
