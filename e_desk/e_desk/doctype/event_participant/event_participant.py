# Copyright (c) 2024, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EventParticipant(Document):
	pass










































# @frappe.whitelist()
# def get_event_participant_count(event=None):
#     if not event:
#         return {"value": 0}
    
#     count = frappe.db.count("Event Participant", filters={"event": event})
    
#     return {
#         "value": count,
#         "fieldtype": "Int"
#     }

