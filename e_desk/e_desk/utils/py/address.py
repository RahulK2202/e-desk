import frappe

def address_link(doc,event):
    links=[]
    for i in doc.links:
        chruch=False
        if i.link_doctype=="Church":
            church=frappe.get_value("Church",i.link_name,"church")
            for j in doc.links:
                if i.link_doctype=="Church" and i.link_name==church and chruch==False:
                    chruch= True
            if chruch==False:
                links.append({"link_doctype":"Church","link_name":church})
    doc.update({
        "links":doc.links+links

    })