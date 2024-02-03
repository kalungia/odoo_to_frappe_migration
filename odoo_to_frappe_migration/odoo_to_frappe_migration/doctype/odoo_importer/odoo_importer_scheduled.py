import frappe
import frappe.www.list
from frappe import _
from odoo_to_frappe_migration.odoo_to_frappe_migration.doctype.odoo_importer.odoo_importer import start_importer
import json


def schedule_importer():

	odooimporter = frappe.db.sql(f" select * from `tabOdoo Importer` where status = 'Ready';""",as_dict=1)	
	
	for rec in odooimporter:
		import_data = start_importer(rec.name)
