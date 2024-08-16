import frappe
import json

<<<<<<< HEAD
<<<<<<< HEAD
=======

@frappe.whitelist()
>>>>>>> 4d8fe7b (updated event participant role and fixed volunteer creation function issues)
=======
@frappe.whitelist()
>>>>>>> db0695a (added role change)
def update_user_role(user, role_name):
    user.update({
        "role_profile_name": role_name,
        "user_type": "System User"
    })
    user.save()
<<<<<<< HEAD
<<<<<<< HEAD
    frappe.db.commit()
=======
    frappe.db.commit()

@frappe.whitelist()
def update_event_particpant_role(doc, confer_id,role_name):
    participant = frappe.get_doc(
        "Event Participant",
        {"parent": confer_id, "participant": doc},
        "name"
    )
    frappe.db.set_value('Event Participant', participant, 'event_role', role_name)
    user = frappe.get_doc('User', {'participant_id': doc})
    update_user_role(user,role_name)


@frappe.whitelist()
def get_filtered_confer(doctype, txt, searchfield, start, page_len, filters):
    participant = filters.get('participant')
    # Query returns a list of tuples instead of a list of dicts
    conf = frappe.db.sql(
         """
=======
    frappe.db.commit()
    
@frappe.whitelist()
def update_event_participant_role(participant,confer, role_name):
    event_participant= frappe.db.get_value('Event Participant', {'parent': confer,'participant':participant}, ['name'])
    frappe.db.set_value('Event Participant', event_participant, 'event_role', role_name, update_modified=False)
    user=frappe.get_doc('User',{'participant_id': participant})
    if user.role_profile_name != "E-Desk Admin":
        update_user_role(user ,role_name)

@frappe.whitelist()
def get_filtered_confer(doctype, txt, searchfield, start, page_len,filters):
    participant = filters.get('participant')
    # Query to get Confer records where the Event Participant has the specific participant
    conf = frappe.db.sql(
        """
>>>>>>> db0695a (added role change)
        SELECT c.name
        FROM `tabConfer` AS c
        JOIN `tabEvent Participant` AS ep ON c.name = ep.parent
        WHERE ep.participant = %(participant)s
        """,
        {
            'participant': participant
        }
    )
<<<<<<< HEAD
    return conf




>>>>>>> 4d8fe7b (updated event participant role and fixed volunteer creation function issues)
=======
    
    return conf
>>>>>>> db0695a (added role change)
