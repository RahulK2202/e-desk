# Copyright (c) 2024, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ConfProgrammeAttendee(Document):
	pass


@frappe.whitelist()
def scanning_validations(doc, programme):
	# Get the parent event (Confer) from the Confer Agenda doctype
	parent_confer = frappe.db.get_value("Confer Agenda", {"name": programme}, "parent")	
	# Check if the participant is registered for the event
	event_participant_id = frappe.db.get_value("Event Participant", {"participant": doc, "event": parent_confer}, "name")
	if not event_participant_id:
		frappe.msgprint("Please scan Event User")
		return None 

	# Check if the user is already scanned for this programme
	scanned_user_exist = frappe.db.exists("Scanned List", {"participant": event_participant_id, "Programme": programme})
	if scanned_user_exist:
		frappe.msgprint(f"User is already scanned for the {programme}")
		return None  # Stop further processing if the user is already scanned

	# If all checks pass, return the participant ID
	full_name = frappe.db.get_value("Participant", doc, "full_name")
	return {
        "event_participant_id": event_participant_id,
        "full_name": full_name
    }

	
