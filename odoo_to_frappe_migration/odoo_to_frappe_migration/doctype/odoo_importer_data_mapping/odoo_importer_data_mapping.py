# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OdooImporterDataMapping(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		data_name: DF.Data
		field_name: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		use_this_data: DF.Check
	# end: auto-generated types

	pass
