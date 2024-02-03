# For license information, please see license.txt
import os

from rq.timeouts import JobTimeoutException


import frappe
import xmlrpc.client
from frappe.utils import getdate
from nameparser import HumanName
from frappe.model.document import Document

class OdooImporter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from ibase.accounts.doctype.odoo_data_fields.odoo_data_fields import OdooDataFields
		from ibase.accounts.doctype.odoo_importer_data_mapping.odoo_importer_data_mapping import OdooImporterDataMapping

		connection_status: DF.SmallText | None
		data_mapping: DF.Table[OdooImporterDataMapping]
		database: DF.Data
		host: DF.Data
		import_from: DF.Int
		total_data: DF.Data
		import_type: DF.Literal["", "Insert New Records", "Update Existing Records"]
		limit: DF.Int
		odoo_data_sample: DF.HTMLEditor | None
		odoo_fields: DF.Table[OdooDataFields]
		odoo_model: DF.Data
		password: DF.Data
		reference_doctype: DF.Link
		status: DF.Literal["Pending", "Connected", "Connection Error", "Ready", "Success", "Partial Success", "Error", "Timed Out"]
		username: DF.Data
	# end: auto-generated types

	pass



@frappe.whitelist()
def oodo_connector(host, database, username, password):
	common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(host))
	uid = common.authenticate(database, username, password, {})
	return uid

@frappe.whitelist()
def odoo_data_sample(docname):
	doc = frappe.get_doc("Odoo Importer", docname)
	field_list = []
	for rec in doc.odoo_fields:
		field_list.append(rec.field_name)
	if not field_list:
		return False

	uid = oodo_connector(doc.host, doc.database, doc.username, doc.password)
	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(doc.host))
	sample_data = models.execute_kw(doc.database, uid, doc.password, doc.odoo_model, 'search_read', [], {'fields': field_list, 'limit': 30})
	countrecords = models.execute_kw(doc.database, uid, doc.password, doc.odoo_model, 'search_count', [])
	doc.total_data = countrecords
	doc.save()	
	return sample_data


@frappe.whitelist()
def start_importer(docname):
	"""This method runs in background job"""
	doc = frappe.get_doc("Odoo Importer", docname)
	try:
		field_list = []
		end_point = int(doc.limit)
		import_from = int(doc.import_from)
		import_from = int(doc.import_from)

		for rec in doc.odoo_fields:
			field_list.append(rec.field_name)
		if not field_list:
			return False

		uid = oodo_connector(doc.host, doc.database, doc.username, doc.password)
		models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(doc.host))

		rnumber = int(end_point - import_from)
		for i in range(rnumber):
			odoodata = models.execute_kw(doc.database, uid, doc.password, doc.odoo_model, 'search_read', [[['id', '=', import_from]]], {'fields': field_list})
			if odoodata:
				if doc.reference_doctype == 'Patient':
					for rec in odoodata:	
						create_patient(docname, rec['name'], rec['gender'], rec['DoB'], rec['id_passport'])
			import_from = import_from + 1
			doc.limit == doc.limit + 1
			doc.import_from == doc.import_from + 1
			doc.save()

			if doc.total_data >= doc.import_from:
				doc.status == 'Success'
				doc.save()

	except JobTimeoutException:
		frappe.db.rollback()
		# data_import.db_set("status", "Timed Out")
	except Exception:
		frappe.db.rollback()
	finally:
		frappe.flags.in_import = False

	frappe.publish_realtime("odoo_importer_refresh", {"odoo_importer": doc.name})




		# 	incre += incre
		# doc.limit = incre
		# doc.save()


@frappe.whitelist()
def create_patient(docname, name, gender=False, DoB=False, id_passport=False):
	patient = frappe.db.exists(doc.reference_doctype, name)
	if not patient:
		doc = frappe.get_doc("Odoo Importer", docname)
		new_doc = frappe.new_doc(doc.reference_doctype)
		fullname = HumanName(name)
		new_doc.first_name = fullname.first
		new_doc.middle_name = fullname.middle
		new_doc.last_name = fullname.last

		if gender == 'M':
			new_doc.sex = 'Male'
		elif gender == 'M':
			new_doc.sex = 'Female'
		else:
			new_doc.sex = 'Other'
		if DoB:
			if DoB != "false" or DoB != False:
				if "false" not in DoB:
					new_doc.dob = getdate(DoB)

		if id_passport:
			new_doc.uid = id_passport

		new_doc.flags.ignore_mandatory = True
		new_doc.flags.ignore_permissions = True
		dos = new_doc.save()
		if dos:
			return True
		else:
			return False
