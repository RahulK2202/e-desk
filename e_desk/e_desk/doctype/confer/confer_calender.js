frappe.views.calendar["Confer Agenda"] = {  
    field_map: {
        "start": "start_date",
        "end": "end_date",
        "id": "name",
        "title": "title",
        "allDay": "all_day"
    },
    gantt: true,
    filters: [
        {
            "fieldtype": "Link",
            "fieldname": "parent",
            "options": "Confer",
            "label": __("Parent")
        }
    ],
    get_events_method: "e_desk.e_desk.doctype.event_participant.event_participant.get_events"
};
