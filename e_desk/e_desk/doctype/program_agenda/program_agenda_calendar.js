frappe.views.calendar["Program Agenda"] = {
	field_map: {
		start: "start",
		end: "end",
		id: "name",
		title: "description",
		allDay: "allDay",
		progress: "progress",
	},
	gantt: true,
	get_events_method: "frappe.desk.calendar.get_events",
};
