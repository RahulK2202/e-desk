# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.core.doctype.user.user import get_role_profile
from frappe.utils import get_datetime, add_to_date , now ,getdate
from datetime import datetime, time, timedelta
from e_desk.e_desk.doctype.registration_desk.registration_desk import RegistrationDesk 
class Participant(Document):
	# @frappe.whitelist(allow_guest=True)
	def after_insert(self):
		if not frappe.db.exists('User',self.e_mail):

			print("this is woreking here.....................................................")
			doc=frappe.new_doc('User')
			doc.update({
				"email":self.e_mail,
				"first_name":self.first_name,
				"last_name":self.last_name,
				"mobile_no":self.mobile_number,
				"new_password":self.mobile_number,
				"send_welcome_email":0,
				"role_profile_name":"Participant",
				"roles":get_role_profile("Participant"),
				"user_type":"System User",
				"module_profile":"E-desk profile",
				"participant_id":self.name

			})
			print(doc,"doc is woreking hereeeeeeeeeeeeeeeeeeee")
			
			doc.save(ignore_permissions=True)
				  
		#attachment inside the participant -> category files
		# category_files=frappe.get_all('Category Table', filters={'parent': self.capacity}, fields=['attach'])
		# self.update({
		# 	"category_files":category_files,
		# })

		
		# if self.is_paid:
		# 	qr=RegistrationDesk.create_qr_participant(self)
		# 	self.status = "Registered"
		# 	self.save()
		
		# permission=frappe.new_doc("User Permission")
		# permission.user=self.e_mail
		# permission.allow='Participant'
		# permission.for_value=self.name
		# permission.save()
		# frappe.db.commit()
	#getting the category file table




	@frappe.whitelist()
	def categoryfile_fetching(doc, a=None):
		category_files=frappe.get_all('Category Table', filters={'parent': 'CCA Settings'}, fields=['attach'])
		doc=frappe.get_doc(doc)
		doc.update({
			"category_files":category_files,
		})
		# doc.save()
		return category_files




	def on_trash(self):
		user_list=frappe.get_list("User",filters={"participant_id":self.name},pluck='name')
		for i in user_list:
			user=frappe.get_doc("User",i)
			user.enabled=0
			user.participant_id=''
			user.save()


	
# Converting the participant to volunteer
@frappe.whitelist()
def volunteer_creation(doc):
	doc=json.loads(doc)
	# v_doc=frappe.new_doc('Volunteer')
	# v_doc.update({
	# 	"e_mail":doc.get('e_mail'),
	# 	"mobile_number":doc.get('mobile_number'),
	# 	"name1":doc.get('full_name'),
	# 	"participant":doc.get('name'),
	# 	"module_profile":"E-desk profile",
	# }),
	# v_doc.save()

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



@frappe.whitelist()

def validate_food(doc):
	food_scan = frappe.db.get_single_value("CCA Settings", "food_scan_hours")

	scanned_time = ''
	buffer_hours = timedelta(hours=food_scan)
	current_time = now()

	if doc:
		doc_par = frappe.get_doc("Participant", doc)
		doc_par.append("food_scan", {
			"datetime":current_time
		})

		if len(doc_par.food_scan) >= 2:
			length = len(doc_par.food_scan)

			scanned_time = doc_par.food_scan[length - 2].datetime
			if scanned_time:
				time_difference = get_datetime(current_time) - get_datetime(scanned_time)
				if time_difference < buffer_hours:
					frappe.throw(f"Food Already Scanned at {scanned_time}")
				else:
					
					doc_par.save()
					doc_par.append("attendance_list", {
						"datetime":current_time
					})

					if len(doc_par.attendance_list) >= 2:
						length = len(doc_par.attendance_list)

						scanned_time = doc_par.attendance_list[length - 2].datetime
						if scanned_time:
							time_difference = get_datetime(current_time) - get_datetime(scanned_time)
							if time_difference < buffer_hours: 
								pass
							else:
								doc_par.save()
					else:
						doc_par.save()
		else:
			doc_par.save()
		
	return doc

@frappe.whitelist()

def validate_attendance(doc):
	attendance_scan = frappe.db.get_single_value("CCA Settings", "attendance_scan_hours")
	frappe.errprint(attendance_scan)
	scanned_time = ''
	buffer_hours = timedelta(hours=attendance_scan)
	current_time = now()

	if doc:
		doc_par = frappe.get_doc("Participant", doc)
		doc_par.append("attendance_list", {
			"datetime":current_time
		})

		if len(doc_par.attendance_list) >= 2:
			length = len(doc_par.attendance_list)

			scanned_time = doc_par.attendance_list[length - 2].datetime
			if scanned_time:
				time_difference = get_datetime(current_time) - get_datetime(scanned_time)
				if time_difference < buffer_hours:
					frappe.throw(f"Attendance Already Scanned at {scanned_time}")
				else:
					doc_par.save()
		else:
			doc_par.save()
		
	return doc
@frappe.whitelist()

def full_address(address):
	hotel=frappe.get_doc("Hotel",address)
	add=frappe.get_doc("Address",hotel.address)
	search_text = ""

	if add.address_title:
		search_text = search_text  + add.address_title
		
	if add.address_line1:
		search_text = search_text + ",<br>"+add.address_line1


	if add.city:
		search_text = search_text + ",<br>" + add.city

	if add.state:
		search_text = search_text + ",<br>" + add.state

	if add.country:
		search_text = search_text + ",<br>" + add.country

	if add.pincode:
		search_text = search_text + ",<br>" + add.pincode
	
	return search_text

@frappe.whitelist()

def full_address_church(address):
	hotel=frappe.get_doc("Church",address)
	add=frappe.get_doc("Address",hotel.address)
	search_text = ""

	if add.address_title:
		search_text = search_text  + add.address_title
		
	if add.address_line1:
		search_text = search_text + ",<br>"+add.address_line1


	if add.city:
		search_text = search_text + ",<br>" + add.city

	if add.state:
		search_text = search_text + ",<br>" + add.state

	if add.country:
		search_text = search_text + ",<br>" + add.country

	if add.pincode:
		search_text = search_text + ",<br>" + add.pincode
	
	return search_text

def atten_food_script():
	participant_lsit=frappe.get_all("Participant")
	for i in participant_lsit:
		participant=frappe.get_doc("Participant",i.name)
		if participant.food_scan:
			for j in participant.food_scan:
				food_scan_date=j.get("datetime").date()
				match=False
				for k in participant.attendance_list:
					att_scan_date=k.get("datetime").date()
					if  food_scan_date==att_scan_date:
						match=True
						break

				if match==False:
					participant.append("attendance_list", {
						"datetime":j.datetime
					})
					participant.save()
					frappe.db.commit()
									