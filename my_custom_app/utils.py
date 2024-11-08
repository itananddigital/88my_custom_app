# my_custom_app/utils.py

import time
import frappe


from frappe.model.naming import make_autoname

def autoname(self, method=None):
	self.name=frappe.generate_hash()[:16]



def log_queries(doc, method):
    # Enable query logging for this session
    frappe.db.sql("SET profiling = 1;")
    frappe.msgprint("Hellow")
    # Run the submission logic
    # This will depend on what you want to do after the invoice is submitted
    # You can trigger additional operations or just finish here

    # Capture the profiling results
    profiles = frappe.db.sql("SHOW PROFILES;", as_dict=True)

    # Log each profile
    for profile in profiles:
        frappe.msgprint("Hellow1")
        query_id = profile['Query_ID']
        execution_time = profile['Duration']

        # Get the query details
        query_details = frappe.db.sql(f"SHOW PROFILE FOR QUERY {query_id};", as_dict=True)

        for detail in query_details:
            query = detail['Query']
            # Log each query execution time into the custom table
            log_entry = frappe.get_doc({
                'doctype': 'Query Execution Log',
                'invoice_id': doc.name,  # or the relevant invoice identifier
                'query': query,
                'execution_time': execution_time,
            })
            log_entry.insert(ignore_permissions=True)

    # Commit the transaction
    frappe.db.commit()

    # Optionally, disable profiling if needed
    frappe.db.sql("SET profiling = 0;")
