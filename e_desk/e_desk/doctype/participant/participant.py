# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class Participant(Document):

	def validate(self):
		if not frappe.db.exists('User',self.e_mail):
			doc=frappe.new_doc('User')
			doc.update({
				"email":self.e_mail,
				"first_name":self.first_name,
				"last_name":self.last_name,
				"mobile_no":self.mobile_number,
				"new_password":self.mobile_number,
				"send_welcome_email":0,
				"role_profile_name":"Participant",
				"user_type":"Website User",
				"module_profile":"E-desk profile",

			}),
			doc.save()
		#attachment inside the participant -> category files
		category_files=frappe.get_all('Category Table', filters={'parent': self.capacity}, fields=['attach'])
		self.update({
			"category_files":category_files,
		})


	
# Converting the participant to volunteer
@frappe.whitelist()
def volunteer_creation(doc):
	doc=json.loads(doc)
	v_doc=frappe.new_doc('Volunteer')
	v_doc.update({
		"e_mail":doc.get('e_mail'),
		"mobile_number":doc.get('mobile_number'),
		"name1":doc.get('first_name')+doc.get('last_name'),
		"participant":doc.get('name'),
		"module_profile":"E-desk profile",
	}),
	v_doc.save()

	# converting the user to volunteer profile
	user=frappe.get_doc("User",doc.get('e_mail'))
	user.update(
		{
			"role_profile_name":"Volunteer",
			"user_type":"System User"
		}
	)
	user.save()
	frappe.db.commit()

#getting the category file table
@frappe.whitelist()
def categoryfile_fetching(capacity_name,doc):
		doc=json.loads(doc)
		category_files=frappe.get_all('Category Table', filters={'parent': capacity_name}, fields=['attach'])
		doc=frappe.get_doc(doc)
		doc.update({
			"category_files":category_files,
		})
		doc.save()
		return category_files