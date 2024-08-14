import frappe

def update_user_role(user, role_name):
    user.update({
        "role_profile_name": role_name,
        "user_type": "System User"
    })
    user.save()
    frappe.db.commit()