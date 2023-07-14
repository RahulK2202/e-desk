# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
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
				"new_password":self.mobile_number,
				"user_type":"Website User",
				"send_welcome_email":0,
				"capacity_file_url":capacity_doc
			}),
			doc.save()
			frappe.db.commit()

		
# Converting the participant to volunteer
@frappe.whitelist()
def volunteer_creation(doc):
	doc=json.loads(doc)
	v_doc=frappe.new_doc('Volunteer')
	v_doc.update({
		"e_mail":doc.get('e_mail'),
		"mobile_number":doc.get('mobile_number'),
		"name1":doc.get('first_name')+doc.get('last_name'),
		"participant":doc.get('name')
	}),
	v_doc.save()

	# converting the user as system user
	user=frappe.get_doc("User",doc.get('e_mail'))
	user.update(
		{
			"role_profile_name":"Participant",
			"user_type":"System User"
		}
	)
	user.save()
	frappe.db.commit()

