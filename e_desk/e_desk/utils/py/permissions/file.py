import frappe

def get_file_permission(user: str = None) -> str:
    user = user or frappe.session.user
    has_role = frappe.get_all("Has Role", filters={"role": 'E-Desk Admin', "parent": frappe.session.user})

    if user == "Administrator" or len(has_role):
        return ""
    return """ `tabFile`.folder like "%GA Drive%" or `tabFile`.file_name = "GA Drive" """

