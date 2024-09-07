# Copyright (c) 2024, sathya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

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
def get_confer_agenda_events(start, end):
    """Fetches the events from Confer Agenda to display in the calendar view."""

    # Step 1: Get parent Confer entries within the date range
    confer_list = frappe.get_all('Confer', filters={
        'start_date': ['<=', end],
        'end_date': ['>=', start]
    }, fields=['name'])

    agenda_events = []
    
    # Step 2: Loop through each Confer and fetch the child table data (Confer Agenda)
    for confer in confer_list:
        agenda = frappe.get_all('Confer Agenda', filters={
            'parent': confer.name,
            'start_date': ['<=', end],
            'end_date': ['>=', start]
        }, fields=['program_agenda', 'start_date', 'end_date'])
        
        # Step 3: Add each agenda item to the calendar data with required fields
        for item in agenda:
            agenda_events.append({
                "title": item.program_agenda,
                "start": item.start_date,
                "end": item.end_date,
                "color": "#FF5733"  # Example color, you can add dynamic logic for different colors
            })
    
    
    return agenda_events











































# @frappe.whitelist()
# def get_event_participant_count(event=None):
#     if not event:
#         return {"value": 0}
    
#     count = frappe.db.count("Event Participant", filters={"event": event})
    
#     return {
#         "value": count,
#         "fieldtype": "Int"
#     }

