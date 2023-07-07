# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import json
import frappe
import io
from frappe.model.document import Document
from pyqrcode import create as qr_create
import os

class RegistrationDesk(Document):
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
	
	def on_update(self):
		for row in self.participant:
			if not row.profile_img:
				frappe.throw(f"Profile picture mandatory in {row.idx}")
			doc = frappe.get_doc("Participant", row.participant_id)
			qr=self.create_qr_participant(doc)
			doc.status = "Registered"
			doc.save()
			frappe.db.set_value(row.doctype, row.name, 'qr_img', qr, update_modified=False)
		self.reload()

	def on_trash(self):
		for row in self.participant:
			doc = frappe.get_doc("Participant", row.participant_id)
			doc.status = "Open"
			doc.save()

	

