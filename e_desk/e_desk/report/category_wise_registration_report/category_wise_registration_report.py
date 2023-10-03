# Copyright (c) 2023, sathya and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [   
		{
			'fieldname': 'category',
			'fieldtype': 'Link',
			'label': 'Category',
			'options': 'Category Name',
			'width': 300
		},
		{
			'fieldname': 'participant',
			'fieldtype': 'Link',
			'label': 'Participant',
			'options': 'Participant',
			'width': 250
		},
		{
			'fieldname': 'participant_name',
			'fieldtype': 'Data',
			'label': 'Participant Name',
			'width': 350
		},
	]
	data = []
	if filters.get("category"):
		participants = frappe.get_all('Participant', {'capacity': ['in',filters.get("category")], 'status': "Registered"})
		if participants:
			sub_data = {
				'category': filters.get("category"),
				'participants': ''
			}
			data.append(sub_data)
			category_participants = []
			for j in participants:
				participant = frappe.get_doc('Participant', j.name)
				category_participants.append({
					'participant': participant.name,
					'participant_name': participant.full_name,
				})
				for k in category_participants:
					sub_data = {
					'category': '',
					'participant': k['participant'],
					'participant_name':k['participant_name'],
					'indent': 1  
				}
				data.append(sub_data)

	else:
		categories = frappe.get_all("Category Name")
		for i in categories:
			participants = frappe.get_all('Participant', {'capacity': ['in', i.name], 'status': "Registered"})
			if participants:
				sub_data = {
					'category': i.name,
					'participants': ''
				}
				data.append(sub_data)
				category_participants = []
				for j in participants:
					participant = frappe.get_doc('Participant', j.name)
					category_participants.append({
						'participant': participant.name,
						'participant_name': participant.full_name,
					})
					for k in category_participants:
						sub_data = {
						'category': '',
						'participant': k['participant'],
						'participant_name':k['participant_name'],
						'indent': 1  
					}
					data.append(sub_data)


	return columns, data
