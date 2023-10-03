# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [   
		{
			'fieldname': 'category',
			'fieldtype': 'Link',
			'label': 'Category',
			'options': 'Category',
			'width': 300
		},
		{
			'fieldname': 'participant',
			'fieldtype': 'Link',
			'label': 'Participant',
			'options': 'Participant',
			'width': 300
		},
		{
			'fieldname': 'participant_name',
			'fieldtype': 'Data',
			'label': 'Participant Name',
			'width': 400
		},
		{
			'fieldname': 'attendance_list',
			'fieldtype': 'Data',
			'label': 'Attendance List',
			'width': 300
		}
	]

	data = [{}]
	if filters.get("from_date") and filters.get("to_date"):
		from_date = filters.get("from_date")
		to_date = filters.get("to_date")
		category = frappe.get_all("Category Name")
		frappe.errprint(category)
		attendance_dict = {}

		for i in category:
			participant = frappe.get_doc('Participant', filters={'capacity': ['in', i.name]})
			if participant:
				frappe.errprint(category)

			
		# 	if participant.attendance_list:
		# 		for attendance in participant.attendance_list:
		# 			attendance_date = attendance.get("datetime")  
		# 			attendance_date = attendance_date.date()  
					
		# 			if from_date <= attendance_date <= to_date:
		# 				if i.name not in attendance_dict:
		# 					attendance_dict[i.name] = []

		# 				attendance_dict[i.name].append(attendance)

		# frappe.errprint(attendance_dict)
						

	return columns, data
