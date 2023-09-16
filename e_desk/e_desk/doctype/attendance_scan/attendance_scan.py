# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime , now 
from datetime import  timedelta
class AttendanceScan(Document):
	pass


@frappe.whitelist()

def validate_attendance(doc):
    
    scanned_time = ''
    buffer_hours = timedelta(hours=24)
    current_time = now()

    if doc:
        doc_par = frappe.get_doc("Participant", doc)
        doc_par.append("attendance_list", {
            "date":current_time
        })

        if len(doc_par.attendance_list) >= 1:
            length = len(doc_par.attendance_list)

            scanned_time = doc_par.attendance_list[length - 2].datetime
            if scanned_time:
                time_difference = get_datetime(current_time) - get_datetime(scanned_time)
                if time_difference < buffer_hours:
                    frappe.throw(f"Already Scanned at {scanned_time}")
                else:
                    
                    doc_par.save()
        else:
            doc_par.save()
        
    return doc