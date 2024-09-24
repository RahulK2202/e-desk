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

    user = frappe.session.user

    agenda_events = []
    if user == "Administrator":
        print("Administrator logged in, showing all events.")
        
        confer_list = frappe.get_all('Confer', filters={
            'start_date': ['<=', end],
            'end_date': ['>=', start]
        }, fields=['name'])

        for confer in confer_list:
            agenda = frappe.get_all('Confer Agenda', filters={
                'parent': confer.name,
                'start_date': ['<=', end],
                'end_date': ['>=', start]
            }, fields=['program_agenda', 'start_date', 'end_date'])

            # Add each agenda item to the calendar data with required fields
            for item in agenda:
                agenda_events.append({
                    "title": item.program_agenda,
                    "start": item.start_date,
                    "end": item.end_date,
                    "color": "#FF5733"  # Static color, you can add dynamic logic
                })
        
        return agenda_events
  
    print(user,"this is the session user")
    participant = frappe.get_value("Participant", {"e_mail": user}, "name") 
    print(participant,"id......................................")
    if not participant:
        # If the user doesn't have a participant ID, return an empty list
        return []
    
    joined_confer_list = frappe.get_all('Event Participant', filters={
        'participant': participant
    }, fields=['event']) 

    joined_confer_ids = [confer['event'] for confer in joined_confer_list]
    print(joined_confer_ids,"joined_confer_idsjoined_confer_idsjoined_confer_ids")

    if not joined_confer_ids:
        # If the user hasn't joined any events, return an empty list
        return []
    
    confer_list = frappe.get_all('Confer', filters={
        'name': ['in', joined_confer_ids],  # Only events the user joined
        'start_date': ['<=', end],
        'end_date': ['>=', start]
    }, fields=['name'])


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


# def has_permission(doc, ptype, user):
#     # Allow Volunteer to access Confer Agenda
#     print("this is the function....................................")
#     if user == "Volunteer" or "Volunteer" in frappe.get_roles(user):
#         return True
#     else:
#         return False



# def conf_programme_attendee_has_permission(doc, user=None, permission_type=None):
#     print("Checking permission for Conf Programme Attendee...")
#     # Allow volunteers to access all actions (read, write, create, delete)
#     if user and "Volunteer" in frappe.get_roles(user):
#         return True
#     return False

# def confer_agenda_has_permission(doc, user=None, permission_type=None):
#     print("Checking permission for Confer Agenda...")
#     # Allow volunteers to access all actions (read, write, create, delete)
#     if user and "Volunteer" in frappe.get_roles(user):
#         return True
#     return False












































