# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Participant(Document):

	def validate(self):
		if not frappe.db.exists('User',self.e_mail):
			doc=frappe.new_doc('User')
			capacity_doc=frappe.get_value("Capacity Name",self.capacity,"capacity_file_url")

			doc.update({
				"email":self.e_mail,
				"first_name":self.first_name,
				"last_name":self.last_name,
				"mobile_no":self.mobile_number,
				"password":self.mobile_number,
				"user_type":"Website User",
				"send_welcome_email":0,
				"capacity_file_url":capacity_doc
			}),
			doc.save()
			frappe.db.commit()