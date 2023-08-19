# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.core.doctype.user.user import get_role_profile
from frappe.utils import get_datetime, add_to_date , now ,getdate
from datetime import datetime, time, timedelta

class Participant(Document):

    def after_insert(self):
        self.full_name=self.first_name+self.last_name
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
                "roles":get_role_profile("Participant"),
                "user_type":"System User",
                "module_profile":"E-desk profile",
                "participant_id":self.name

            })
            doc.save()
            frappe.errprint(doc.user_type)
        #attachment inside the participant -> category files
        category_files=frappe.get_all('Category Table', filters={'parent': self.capacity}, fields=['attach'])
        self.update({
            "category_files":category_files,
        })
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

@frappe.whitelist()

def validate_food(doc):
    scanned_time = ''
    buffer_hours = timedelta(hours=2)
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
                    frappe.throw(f"Already Scanned at {scanned_time}")
                else:
                    
                    doc_par.save()
        else:
            doc_par.save()