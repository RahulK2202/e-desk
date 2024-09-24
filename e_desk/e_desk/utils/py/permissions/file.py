import frappe

# def get_file_permission(user: str = None) -> str:
#     user = user or frappe.session.user
#     has_role = frappe.get_all("Has Role", filters={"role": 'E-Desk Admin', "parent": frappe.session.user})

#     if user == "Administrator" or len(has_role):
#         return ""
#     return """ `tabFile`.folder like "%GA Drive%" or `tabFile`.file_name = "GA Drive" """

def get_file_permission(user: str = None) -> str:
    user = user or frappe.session.user
    print(user,"user.........................................")

    # Check if user has the 'E-Desk Admin' role
    has_role = frappe.db.exists("Has Role", {"role": "E-Desk Admin", "parent": user})

    # If the user is Administrator or has the 'E-Desk Admin' role, return no condition (full access)
    if user == "Administrator" or has_role:
        return ""

    # Get participant ID from the Participant doctype using the user's email
    participant_id = frappe.db.get_value("Participant", {"e_mail": user}, "name")
    print( participant_id," participant_id participant_id")

    # If participant ID exists, fetch the events the user is registered for
    if participant_id:
        event_names = frappe.db.get_list(
            "Event Participant",
            filters={"participant": participant_id},
            fields=["event"],
            pluck="event"  # Get a list of event names (folder names)
        )

        print(event_names,"event........................................................")

        # If the user is registered for events, construct the folder condition
        if event_names:
            # Create SQL condition to allow access to folders matching the event names
            folder_conditions = " OR ".join([f"`tabFile`.folder = '{event}'" for event in event_names])
            print(folder_conditions,"folder_conditionsfolder_conditions")
            return f"({folder_conditions})"
        

    # If the user is not registered for any event or no access, return a condition that blocks everything
    return "1 = 0"  # Blocks access by returning a false condition
