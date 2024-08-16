# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
import frappe
import io
from frappe.model.document import Document
from pyqrcode import create as qr_create
import os
from frappe.model.naming import parse_naming_series
<<<<<<< HEAD
<<<<<<< HEAD
from e_desk.e_desk.utils.role import update_user_role
=======
from e_desk.e_desk.utils.role import update_event_particpant_role
>>>>>>> 4d8fe7b (updated event participant role and fixed volunteer creation function issues)
=======
from e_desk.e_desk.utils.role import update_event_participant_role
>>>>>>> db0695a (added role change)

class RegistrationDesk(Document):
    @classmethod
    def create_qr_participant(self, pr_doc):
        qr_image = io.BytesIO()
        data={"e_mail":pr_doc.e_mail,"mobile_number":pr_doc.mobile_number,"name":pr_doc.name}
        data=json.dumps(data,indent=4,sort_keys=True,default=str)
        data_ = qr_create(data, error='L')
        data_.png(qr_image, scale=4, quiet_zone=1)
        name = frappe.generate_hash('', 5)
        filename = f"QRCode-{name}.png".replace(os.path.sep, "__")
        _file = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "is_private": 0,
        "content": qr_image.getvalue(),
        "attached_to_doctype":  pr_doc.doctype,
        "attached_to_name": pr_doc.name,
        "attached_to_field":"qr"
        })
        for i in frappe.get_all("File", {
        "attached_to_doctype":  pr_doc.doctype,
        "attached_to_name": pr_doc.name,
        "attached_to_field":"qr"}):
            frappe.delete_doc("File", i.name)

        _file.save(ignore_permissions=True)
        frappe.db.set_value(pr_doc.doctype, pr_doc.name, 'qr', _file.file_url, update_modified=False)
        pr_doc.reload()
        return _file.file_url
    
    # Registration completed -> converting the participant status as registered
    def on_update(self):
        for row in self.participant:
            if not row.profile_img:
                frappe.throw(f"Profile picture mandatory in {row.idx}")
            doc = frappe.get_doc("Participant", row.participant_id)
            qr=self.create_qr_participant( doc)
            doc.status = "Registered"
            doc.save()
            frappe.db.set_value(row.doctype, row.name, 'qr_img', qr, update_modified=False)
        self.reload()

    # Registration canceled -> moving the particioant to old status
    def on_trash(self):
        for row in self.participant:
            doc = frappe.get_doc("Participant", row.participant_id)
            doc.status = "Open"
            doc.save()
   
    def autoname(self):
        if self.participant:
            first_item =self.participant[0]
            first_item_name=first_item.participant_name
            self.name = parse_naming_series(f"{first_item_name}-.#")

    def on_submit(doc):
<<<<<<< HEAD
        
=======
        participant= doc.participant[0].participant_id
>>>>>>> db0695a (added role change)
        new_row = frappe.get_doc({
            'doctype': 'Event Participant',
            'parenttype': 'Confer',
            'parentfield': 'event_participant',
            'parent': doc.confer,
<<<<<<< HEAD
            'participant': doc.participant[0].participant_id
=======
            'participant': participant,
            'event_role' : "Participant"
>>>>>>> db0695a (added role change)
        })
<<<<<<< HEAD

 
        new_row.save()
        # if user.role_profile_name not in ["Participant", "E-Desk Admin"]:
        update_event_participant_role(participant,doc.confer, "Participant")
            
        frappe.msgprint('Conference updated successfully.')

<<<<<<< HEAD


















=======
>>>>>>> 4d8fe7b (updated event participant role and fixed volunteer creation function issues)
    
        new_row.save()
        update_event_particpant_role(doc.participant[0].participant_id ,doc.confer,"Participant")
        frappe.msgprint(' Registered successfully.')


=======
>>>>>>> db0695a (added role change)
@frappe.whitelist()
def event_participant_filter(doctype, txt, searchfield, start, page_len, filters):
    conference = filters.get('conference')

    # filtering  participant which are not registered in this perticular event
    participants = frappe.db.sql("""
        SELECT p.name
        FROM `tabParticipant` p
        WHERE p.name NOT IN (
            SELECT ep.participant
            FROM `tabEvent Participant` ep
            WHERE ep.parent = %(conference)s
        )
        AND p.name LIKE %(txt)s
        LIMIT %(start)s, %(page_len)s
    """, {
        'conference': conference,
        'txt': "%" + txt + "%",
        'start': start,
        'page_len': page_len
    })


    return participants
