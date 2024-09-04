# Copyright (c) 2024, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EventParticipant(Document):
	pass


@frappe.whitelist()
def count_event():
    print("WELCOME TO THE EVENT...............................................")
    # Fetch the event value from CCA Settings
    event = frappe.db.get_single_value('Conferrx Settings', 'event')
    
    # Count the number of Event Participants linked to the fetched event
    count = frappe.db.count('Event Participant', {'event': event, 'status': 'Open'})

    # Return the count in the required format
    return {
        "value": count,
        "fieldtype": "Int",
        "route_options": {"event": event},
        "route": ["List", "Event Participant", {"event": event}]
    }


@frappe.whitelist()
def count_participant_registered():
    event = frappe.db.get_single_value('Conferrx Settings', 'event')
    
    # Count the number of Event Participants linked to the fetched event
    count = frappe.db.count('Event Participant', {'event': event, 'status': 'Registered'})

    # Return the count in the required format
    return {
        "value": count,
        "fieldtype": "Int",
        "route_options": {"event": event},
        "route": ["List", "Event Participant", {"event": event}]
    }




@frappe.whitelist()
def count_volunteer_registered():
    event = frappe.db.get_single_value('Conferrx Settings', 'event')
    
    # Count the number of Event Participants linked to the fetched event
    count = frappe.db.count('Event Participant', {'event': event, 'status': 'Registered','event_role':"Volunteer"})

    # Return the count in the required format
    return {
        "value": count,
        "fieldtype": "Int",
        "route_options": {"event": event},
        "route": ["List", "Event Participant", {"event": event}]
    }


@frappe.whitelist()
def get_events(start, end, filters=None):
    print("Helloo its reached............................")
    print(start, end,"start, end,start, end,start, end,start, end,")
    events = []
    # Fetch events from the child table
    child_table_entries = frappe.get_all("Confer Agenda", filters={
        "parent": filters.get("parent"),
        "start_date": ["between", [start, end]]
    })
    print(child_table_entries,"child_table_entrieschild_table_entrieschild_table_entrieschild_table_entries")
    for entry in child_table_entries:
        events.append({
            "name": entry.name,
            "start": entry.start_date,
            "end": entry.end_date,
            "title": entry.title,
            "allDay": entry.all_day
        })
    return events










































# @frappe.whitelist()
# def get_event_participant_count(event=None):
#     if not event:
#         return {"value": 0}
    
#     count = frappe.db.count("Event Participant", filters={"event": event})
    
#     return {
#         "value": count,
#         "fieldtype": "Int"
#     }

